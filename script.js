let combinedData = {
    "rikishi_list": [],
    "ratings": [],
    "matches": []
};

// ページ読み込み時にデータを取得
document.addEventListener('DOMContentLoaded', function() {
    loadCombinedData();
    setupNavigation();
});

// ナビゲーションボタンの設定
function setupNavigation() {
    document.getElementById('ratings-page-btn').addEventListener('click', () => showPage('ratings-page'));
    document.getElementById('matches-page-btn').addEventListener('click', () => showPage('matches-page'));
    document.getElementById('rikishi-page-btn').addEventListener('click', () => showPage('rikishi-page'));
}

function showPage(pageId) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        if (page.id === pageId) {
            page.style.display = 'block';
        } else {
            page.style.display = 'none';
        }
    });
}

// データの読み込み
function loadCombinedData() {
    fetch('data/combined_data.json')
        .then(response => response.json())
        .then(data => {
            combinedData = data;
            populateBashoSelects();
            setupRatingsPage();
            setupMatchesPage();
            setupRikishiPage();
        })
        .catch(error => console.error('Error loading combined_data.json:', error));
}

// レーティングページの初期設定
function setupRatingsPage() {
    const bashoSelect = document.getElementById('ratings-basho-select');
    bashoSelect.addEventListener('change', function() {
        const basho = this.value;
        if (basho) {
            displayRatingsTable(basho);
        } else {
            clearRatingsTable();
        }
    });
}

// マッチページの初期設定
function setupMatchesPage() {
    const bashoSelect = document.getElementById('matches-basho-select');
    const daySelect = document.getElementById('matches-day-select');
    
    // Basho選択時にDayのオプションを更新
    bashoSelect.addEventListener('change', function() {
        const basho = this.value;
        populateDaySelect(basho);
        clearMatchesTable();
    });

    // Day選択時にマッチを表示
    daySelect.addEventListener('change', function() {
        const basho = bashoSelect.value;
        const day = this.value;
        if (basho && day) {
            displayMatchesTable(basho, day);
        } else {
            clearMatchesTable();
        }
    });
}

// 力士ページの初期設定
function setupRikishiPage() {
    document.getElementById('rikishi-search-btn').addEventListener('click', function() {
        const input = document.getElementById('rikishi-input').value.trim();
        if (input) {
            const rikishi = findRikishiByName(input);
            if (rikishi) {
                displayRikishiChart(rikishi.ID);
            } else {
                alert('該当する力士が見つかりません。');
            }
        }
    });
}

// Bashoセレクトのポピュレート
function populateBashoSelects() {
    const ratingsBashoSelect = document.getElementById('ratings-basho-select');
    const matchesBashoSelect = document.getElementById('matches-basho-select');
    
    const bashos = Array.from(new Set(combinedData.ratings.map(r => r.Basho)));
    bashos.sort();

    bashos.forEach(basho => {
        const option1 = document.createElement('option');
        option1.value = basho;
        option1.text = basho;
        ratingsBashoSelect.add(option1);

        const option2 = document.createElement('option');
        option2.value = basho;
        option2.text = basho;
        matchesBashoSelect.add(option2);
    });
}

// Dayセレクトのポピュレート
function populateDaySelect(basho) {
    const daySelect = document.getElementById('matches-day-select');
    daySelect.innerHTML = '<option value="">--選択してください--</option>'; // リセット

    const days = Array.from(new Set(
        combinedData.matches
            .filter(m => m.BashoId === basho)
            .map(m => m.Day)
    ));
    days.sort((a, b) => parseInt(a) - parseInt(b));

    days.forEach(day => {
        const option = document.createElement('option');
        option.value = day;
        option.text = day;
        daySelect.add(option);
    });
}

// レーティングテーブルの表示
function displayRatingsTable(basho) {
    const tableBody = document.querySelector('#ratings-table tbody');
    tableBody.innerHTML = ''; // クリア

    const ratings = combinedData.ratings.filter(r => r.Basho === basho);
    // ランキング順にソート（降順）
    ratings.sort((a, b) => b.ratings[14] - a.ratings[14]);

    ratings.forEach((r, index) => {
        const row = document.createElement('tr');

        // 順位
        const rankCell = document.createElement('td');
        rankCell.textContent = index + 1;
        row.appendChild(rankCell);

        // 力士名
        const nameCell = document.createElement('td');
        nameCell.textContent = r.Shikona;
        row.appendChild(nameCell);

        // レーティング
        const ratingCell = document.createElement('td');
        ratingCell.textContent = r.ratings[14]; // 15日目のレーティング
        row.appendChild(ratingCell);

        tableBody.appendChild(row);
    });
}

// レーティングテーブルのクリア
function clearRatingsTable() {
    const tableBody = document.querySelector('#ratings-table tbody');
    tableBody.innerHTML = '';
}

// マッチテーブルの表示
function displayMatchesTable(basho, day) {
    const tableBody = document.querySelector('#matches-table tbody');
    tableBody.innerHTML = ''; // クリア

    const matches = combinedData.matches.filter(m => m.BashoId === basho && m.Day === day);
    matches.sort((a, b) => parseInt(a.MatchNo) - parseInt(b.MatchNo));

    matches.forEach(match => {
        const row = document.createElement('tr');

        // 試合番号
        const matchNoCell = document.createElement('td');
        matchNoCell.textContent = match.MatchNo;
        row.appendChild(matchNoCell);

        // 東力士
        const eastCell = document.createElement('td');
        eastCell.textContent = match.EastShikona;
        row.appendChild(eastCell);

        // 西力士
        const westCell = document.createElement('td');
        westCell.textContent = match.WestShikona;
        row.appendChild(westCell);

        // 決まり手
        const kimariteCell = document.createElement('td');
        kimariteCell.textContent = match.Kimarite;
        row.appendChild(kimariteCell);

        // 勝者
        const winnerCell = document.createElement('td');
        winnerCell.textContent = match.WinnerJp;
        row.appendChild(winnerCell);

        tableBody.appendChild(row);
    });
}

// マッチテーブルのクリア
function clearMatchesTable() {
    const tableBody = document.querySelector('#matches-table tbody');
    tableBody.innerHTML = '';
}

// 力士の検索
function findRikishiByName(name) {
    return combinedData.rikishi_list.find(r => 
        r.Shikona_JP.toLowerCase() === name.toLowerCase() || 
        r.Shikona_EN.toLowerCase() === name.toLowerCase()
    );
}

// 力士のレーティングチャートの表示
function displayRikishiChart(rikishiID) {
    const rikishiRatings = combinedData.ratings.filter(r => r.RikishiID === rikishiID);
    rikishiRatings.sort((a, b) => a.Basho.localeCompare(b.Basho));

    const labels = rikishiRatings.map(r => r.Basho);
    const data = rikishiRatings.map(r => r.ratings[14]); // 15日目のレーティング

    const ctx = document.getElementById('rikishi-rating-chart').getContext('2d');

    if (window.rikishiChart) {
        window.rikishiChart.destroy();
    }

    window.rikishiChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Elo Rating',
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}
