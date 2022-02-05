# caluculate rikishi's rating based on Elo rating
# Elo rating is the traditional calculation of rating




import urllib.error
import numpy as np
import pandas as pd
import sys
import datetime
eps = 1e-9


def readcsv(filenames=["results.csv"], outhtml=False):
    tdf = []
    for filename in filenames:
        tdf.append(pd.read_csv(filename))
    df = pd.concat(tdf)
    results = df[["higashi_id", "option1", "nishi_id", "option2", "higashi_wins", "higashi_loses"]].fillna("").values

    engine_name_withopt = []
    engine_name = []
    opt_value = []
    engine_dict = {}
    opttag = "__option__"
    K = 0
    for i in range(len(results)):
        for j in range(2):
            if not results[i][j * 2] + opttag + results[i][j * 2 + 1] in engine_name_withopt:
                engine_name.append(results[i][j * 2])
                opt_value.append(results[i][j * 2 + 1])
                engine_name_withopt.append(results[i][j * 2] + "__option__" + results[i][j * 2 + 1])
                engine_dict.update({results[i][j * 2] + "__option__" + results[i][j * 2 + 1]: K})
                K += 1
    W = np.zeros([K, K])

    d = datetime.datetime.today()
    if outhtml:
        fp = open("match_log2.html", "w")
        # fp.write("data generated : "+ str(d.day) + "/" + str(d.month) +"/"+ str(d.year)+"   total games: "+ str(int(games/2)))
        fp.write(
            "<style>table {border-collapse: collapse;}th {border: solid 1px #666666;color: #000000;background-color: #ff9999;}td {border: solid 1px #666666;color: #000000;background-color: #ffffff;}thead th {background-color: #9AF6FF;}</style><table><thead><tr><th>engine 1</th><th>engine 2</th><th>1 win</th><th>2 win</th><th>rate diff</th></tr></thead><tbody>")

    for result in results:
        W[engine_dict[result[0] + opttag + result[1]], engine_dict[result[2] + opttag + result[3]]] += float(
            result[4])
        W[engine_dict[result[2] + opttag + result[3]], engine_dict[result[0] + opttag + result[1]]] += float(
            result[5])
        if outhtml:
            fp.write("<tr><td>" + result[0] + "</td> <td>" + result[2] + "</th> <td>" + str(
                result[4]) + "</th> <td>" + str(result[5]) + "</th> <td>" + str(
                int(400. * np.log10(result[4] / result[5]))) + "</tr>\n")
    if outhtml:
        fp.write("</tbody></table>\n")

    # print(W)
    return W, engine_name, opt_value

# resampling data
def resampling_data(data, m, n_trial):
    K = data.shape[0]
    prob = data.reshape([K * K])
    prob /= np.sum(prob)
    samples = np.random.multinomial(m, prob, n_trial)
    return samples.reshape([n_trial, K, K])

class bt_model:
    def __init__(self, data, p_init=None):
        self.data = data
        self.K = data.shape[0]
        self._wi = np.sum(self.data, axis=1)
        self._nij = self.data + np.transpose(self.data)
        if p_init is None:
            self.p = np.ones([self.K]) / self.K
        else:
            self.p = p_init
        return

    def estimate(self):
        diag = np.zeros([self.K, self.K])
        inv_p = np.zeros([self.K, self.K])
        err = 0.0
        for i in range(200):
            prev = self.p
            diag = np.matmul(np.diag(self.p), np.ones([self.K, self.K]))
            inv_p = 1. / (diag + np.transpose(diag))
            np.fill_diagonal(inv_p, 0)

            self.p = self._wi / np.sum(self._nij * inv_p, axis=1)
            self.p /= np.sum(self.p)

            err = abs(np.linalg.norm(self.p - prev))
            if (err < self.eps):
                break
        return

    def get_beta_with_bias(self, i, bias):
        beta = 400 * np.log10(self.p)
        beta += (bias - beta[i])
        return beta

def calcrate(filenames, outhtml=True, outcsv=True):
    data, names, opts = readcsv(filenames, outhtml=outhtml)
    K = data.shape[0]
    n_games = np.sum(data + np.transpose(data), axis=0)
    d = datetime.datetime.today()

    m = int(np.sum(data) * 0.9)

    n_trial = 100
    np.random.seed(634)

    samples = resampling_data(data, m, n_trial)

    p_init = np.ones([K]) / K
    betas = np.zeros([n_trial, K])
    for k in np.arange(n_trial):
        bt = bt_model(samples[k, :, :], p_init)
        bt.estimate()
        betas[k, :] = bt.get_beta_with_bias(0, 3250)
        p_init = bt.p

    # Statistics of rating
    q_25 = np.percentile(betas, 25, axis=0)
    q_50 = np.percentile(betas, 50, axis=0)
    q_75 = np.percentile(betas, 75, axis=0)

    # Sort by rating
    result = np.c_[range(K), q_50, q_75 - q_50, q_50 - q_25, n_games]
    index_s = (-result[:, 1]).argsort()
    result_s = result[index_s]

    games = 0;
    for k in range(K):
        games = games + result_s[k, 4]
    print("done : " + str(games) + " games")

    if outcsv:
        f = open("output" + str(d.year) + "-" + str(d.month) + "-" + str(d.day) + ".csv", 'w')
        f.write("engine,option,rate,error_plus,error_minus,battles\n")
        for k in range(K):
            f.write(names[index_s[k]] + "," + opts[index_s[k]] + "," + str(int(result_s[k, 1])) + "," + str(
                int(result_s[k, 2])) + "," + str(int(result_s[k, 3])) + "," + str(int(result_s[k, 4])) + "\n")
        f.close()

    if outhtml:
        with open("result-s2.html", "w") as fp:
            fp.write("" + str(d.year) + "/" + str(d.month) + "/" + str(d.day) + " " + str(int(games / 2)))
            fp.write(
                "<style> table {border-collapse: collapse;} th {border: solid 1px #666666;color: #000000;background-color: #F6FF9A;}td {border: solid 1px #666666;color: #000000;background-color: #ffffff;}thead th {background-color: #CDFF9A;}</style><table><thead><tr><th>software</th><th>rating</th><th>error</th><th>games</th></tr></thead><tbody>")

            for k in range(K):
                if opts[index_s[k]].find("+") != -1:
                    fp.write("<tr><th>" + names[
                        index_s[k]] + "</th> <td>{1:d}</td> <td> +{2:d}/-{3:d} </td><td> {0:d}</td>".format(
                        int(result_s[k, 4]), int(result_s[k, 1]), int(result_s[k, 2]),
                        int(result_s[k, 3])) + "</tr>\n")
            fp.write("</tbody></table>\n")

        with open("result-e2.html", "w") as fp:
            fp.write("data generated : " + str(d.day) + "/" + str(d.month) + "/" + str(
                d.year) + "   total games: " + str(int(games / 2)))
            fp.write(
                "<style> table {border-collapse: collapse;} th {border: solid 1px #666666;color: #000000;background-color: #F6FF9A;}td {border: solid 1px #666666;color: #000000;background-color: #ffffff;}thead th {background-color: #CDFF9A;}</style><table><thead><tr><th></th><th></th><th></th><th></th></tr></thead><tbody>")

            for k in range(K):
                fp.write("<tr><th>" + names[
                    index_s[k]] + "</th> <td>{1:d}</td> <td> +{2:d}/-{3:d} </td><td> {0:d}</td>".format(
                    int(result_s[k, 4]), int(result_s[k, 1]), int(result_s[k, 2]), int(result_s[k, 3])) + "</tr>\n")
            fp.write("</tbody></table>\n")

if __name__ == "__main__":
    args = []
    if len(sys.argv) < 2:
        print("usage python ratecalc.py target_csv_name.csv")
    else:
        for i in range(len(sys.argv) - 1):
            args.append(sys.argv[i + 1])
        calcrate(args)
