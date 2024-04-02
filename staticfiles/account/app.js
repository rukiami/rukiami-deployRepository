document.addEventListener('DOMContentLoaded', function () {
    // CSRFトークンを取得するための関数
        function getCSRFToken() {
            const token = document.querySelector('input[name="csrfmiddlewaretoken"]') ? 
                          document.querySelector('input[name="csrfmiddlewaretoken"]').value : '';
            return token;
        }    
           // CSRFトークンをaxiosのデフォルトヘッダーに設定
        axios.defaults.headers.common['X-CSRFToken'] = getCSRFToken();
        var calendarEl = document.getElementById('calendar');
    
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            selectable: true,
    
            select: function (info) {
                // イベント名の入力ダイアログ
                const eventName = prompt("イベントを入力してください");
                if (eventName) {
                    // サーバーにイベントを追加するPOSTリクエスト
                    axios.post('/account/add_event/', {
                        event_name: eventName,
                        start_date: info.start.valueOf(), // UTCのタイムスタンプに変換
                        end_date: info.end.valueOf(), // UTCのタイムスタンプに変換
                    })
                    .then(function (response) {
                        if (response.data.status === 'success') {
                            // イベントの追加が成功したらカレンダーに表示
                            calendar.addEvent({
                                title: eventName,
                                start: info.start,
                                end: info.end,
                                allDay: true,
                            });
                            alert('イベントが追加されました');
                        } else {
                            alert('イベントの追加に失敗しました');
                        }
                    })
                    .catch(function (error) {
                        console.log(error);
                        alert('イベントの追加中にエラーが発生しました');
                    });
                }
            },
    
            // カレンダーのイベントを動的に取得
            events: function (info, successCallback, failureCallback) {
                axios.post('/account/get_events/', {
                    start_date: info.start.valueOf(), // UTCのタイムスタンプに変換
                    end_date: info.end.valueOf(), // UTCのタイムスタンプに変換
                })
                .then(function (response) {
                    successCallback(response.data);
                })
                .catch(function (error) {
                    console.log(error);
                    failureCallback(error);
                });
            },
        });
    
        calendar.render();
    });
    