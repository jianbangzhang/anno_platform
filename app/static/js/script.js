document.addEventListener('DOMContentLoaded', (event) => {
    const toggleBtn = document.getElementById('toggle-btn');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('hide');
        content.classList.toggle('full');
    });

    window.loadContent = function(page) {
        fetch(`/${page}`)
            .then(response => response.text())
            .then(html => {
                content.innerHTML = html;
            })
            .catch(error => {
                console.warn('Error loading content:', error);
            });
    }
});

console.log("JavaScript loaded");

document.addEventListener('DOMContentLoaded', function() {
    fetch('/data_overview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('data-management');
        if (data.length > 0) {
            let table = document.createElement('table');
            let headerRow = document.createElement('tr');
            headerRow.innerHTML = `
                <th>版本</th>
                <th>数据名称</th>
                <th>数据量</th>
                <th>导入时间</th>
                <th>标注类型</th>
                <th>标注状态</th>
                <th>清洗状态</th>
                <th>操作</th>
            `;
            table.appendChild(headerRow);

            data.forEach(item => {
                let row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.version}</td>
                    <td>${item.data_name}</td>
                    <td>${item.data_size}</td>
                    <td>${item.upload_time}</td>
                    <td>${item.data_type}</td>
                    <td>${(100*item.anno_percent/item.data_size).toFixed(2)}% (${item.anno_percent}/${item.data_size})</td>
                    <td>-</td>
                    <td>
                        <a href="#" class="load-button" data-file="${item.file_path}">加载</a>
                        <a href="/export?file=${item.file_path}" class="export-button" data-file="${item.file_path}">导出</a>
                        <a href="#" class="delete-button" data-file="${item.file_path}">删除</a>
                    </td>
                `;
                table.appendChild(row);
            });

            container.appendChild(table);

            // Add event listeners for load buttons
            const loadButtons = document.querySelectorAll('.load-button');
            loadButtons.forEach(button => {
                button.addEventListener('click', function(event) {
                    event.preventDefault();
                    const filePath = this.getAttribute('data-file');
                    fetch(`/load?file=${encodeURIComponent(filePath)}`)
                        .then(response => response.json())
                        .then(data => {
                            alert(`已经成功加载数据！`);
                        });
                });
            });

            // Add event listeners for delete buttons
            const deleteButtons = document.querySelectorAll('.delete-button');
            deleteButtons.forEach(button => {
                button.addEventListener('click', function(event) {
                    event.preventDefault();
                    const filePath = this.getAttribute('data-file');
                    deleteFile(filePath);
                });
            });
        }
    });

    function deleteFile(filePath) {
        if (confirm("确定要删除这个文件吗？")) {
            fetch('/file_delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `filePath=${encodeURIComponent(filePath)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "文件已成功删除") {
                    alert(data.message);
                    location.reload(); // 刷新页面以更新表格
                } else {
                    alert("删除文件失败: " + data.message);
                }
            })
            .catch(error => {
                alert("删除文件失败: " + error);
            });
        }
    }
});



function deleteFile(filePath) {
    // 确认是否删除文件
    if (confirm("确定要删除这个文件吗？")) {
        // 创建XMLHttpRequest对象
        var xhr = new XMLHttpRequest();
        // 设置请求类型和URL
        xhr.open("POST", "/file_delete", true);
        // 设置请求头
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        // 发送请求并附带文件路径数据
        xhr.send("filePath=" + encodeURIComponent(filePath));

        // 处理请求响应
        xhr.onload = function() {
            if (xhr.status == 200) {
                alert("文件已成功删除");
                location.reload(); // 刷新页面以更新表格
            } else {
                alert("示例文件不可删除！");
            }
        };
    }
}


document.getElementById('dataset-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData();
    formData.append('dataset-name', document.getElementById('dataset-name').value);
    formData.append('dataset-type', document.getElementById('dataset-type').value);
    formData.append('dataset-version', document.getElementById('dataset-version').value);
    formData.append('file', document.getElementById('dataset-file').files[0]);

    fetch('/upload_data', {
        method: 'POST',
        body: formData
    })
    .then(async response => {
        var messageDiv = document.getElementById('message');
        const data = await response.json();
        if (response.ok) {
            messageDiv.innerHTML = '<p class="flash-message success">' + data.message + '</p>';
        } else {
            alert(data.message);
            messageDiv.innerHTML = '<p class="flash-message error">' + data.message + '</p>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(data.message);
        var messageDiv = document.getElementById('message');
        messageDiv.innerHTML = '<p class="flash-message error">文件上传失败: ' + error.message + '</p>';
    });
});


// 新增的调用Agent函数
function callAgent() {
    const inputText = document.getElementById('input-text').value;
    fetch('/call_agent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: inputText })
    }).then(response => response.json())
    .then(data => {
        document.getElementById('output-text').value = data.output;
    }).catch(error => {
        console.error('Error:', error);
        alert('调用Agent失败');
    });
}

function callAgent1() {
    const inputText = document.getElementById('output-prompt').value;
    fetch('/call_agent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: inputText })
    }).then(response => response.json())
    .then(data => {
        document.getElementById('output-text1').value = data.output;
    }).catch(error => {
        console.error('Error:', error);
        alert('调用Agent失败');
    });
}

function generatePrompt() {
    const selectedScene = document.getElementById('scene-select').value;
    const userInput = document.getElementById('user-input').value;

    fetch('/generate_prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            scene: selectedScene,
            input: userInput
        })
    }).then(response => response.json())
    .then(data => {
        document.getElementById('output-prompt').value = data.prompt;
    }).catch(error => {
        console.error('Error:', error);
        alert('生成Prompt失败');
    });
}

document.getElementById('scene-select').addEventListener('change', function() {
    var selectedOption = this.options[this.selectedIndex].text;
    document.getElementById('scene-text').innerText = '当前选择的场景是：' + selectedOption;
});

// 默认加载天气查询
window.onload = function() {
    var selectElement = document.getElementById('scene-select');
    selectElement.value = '天气查询';
    var event = new Event('change');
    selectElement.dispatchEvent(event);
};


// 点击页面其他地方时关闭下拉菜单
window.onclick = function(event) {
    if (!event.target.matches('.username')) {
        var dropdown = document.getElementById('dropdown');
        if (dropdown.style.display === 'block') {
            dropdown.style.display = 'none';
        }
    }
}

//chat

function sendMessage() {
    var input = document.getElementById('chat-input');
    var message = input.value;
    if (message.trim() === '') return;

    // 将用户消息添加到聊天框中
    var chatBox = document.getElementById('chat-box');
    var userMessage = document.createElement('div');
    userMessage.textContent = '用户: ' + message;
    chatBox.appendChild(userMessage);

    // 清空输入框
    input.value = '';

    // 发送消息到服务器
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    }).then(response => response.json()).then(data => {
        // 将服务器回复添加到聊天框中
        var botMessage = document.createElement('div');
        botMessage.textContent = 'Agent: ' + data.reply;
        chatBox.appendChild(botMessage);

        // 滚动到聊天框底部
        chatBox.scrollTop = chatBox.scrollHeight;
    }).catch(error => {
        console.error('Error:', error);
    });
}


function toggleDropdown() {
    var dropdown = document.getElementById('dropdown');
    if (dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
    } else {
        dropdown.style.display = 'block';
    }
}

function logout() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) {
            window.location.href = '/';
        } else {
            alert('退出登录失败');
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('退出登录失败');
    });
}

// 点击页面其他地方时关闭下拉菜单
window.onclick = function(event) {
    if (!event.target.matches('.username')) {
        var dropdown = document.getElementById('dropdown');
        if (dropdown.style.display === 'block') {
            dropdown.style.display = 'none';
        }
    }
}



document.getElementById('prev-btn').addEventListener('click', function () {
    if (currentIndex > 0) {
        fetchData(currentIndex - 1);
    }
});

document.getElementById('next-btn').addEventListener('click', function () {
    fetchData(currentIndex + 1);
});




function searchData() {
    const query = document.getElementById("searchInput").value;

    fetch('/data_retrieval_search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: query }),
    })
    .then(response => response.json())
    .then(data => {
        const resultContainer = document.getElementById("resultContainer");
        resultContainer.innerHTML = ''; // 清空之前的结果

        if (data.length === 0) {
            resultContainer.innerHTML = '<div class="no-results">未查询到相关数据</div>';
        } else {
            const table = document.createElement("table");
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>序号</th>
                        <th>原始数据</th>
                        <th>标注数据</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            `;
            const tbody = table.querySelector("tbody");

            const allIds = data.map(item => item.id);

            data.forEach((item, index) => {
                const highlightedText = highlightKeyword(item.text, query);
                const highlightedResult = highlightKeyword(item.result, query);

                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${highlightedText}</td>
                    <td>${highlightedResult}</td>
                    <td>
                        <div class="vertical-text">
                            <a href="#" onclick="deleteSearchItem(${item.id})">删除</a>
                            <a href="#" onclick="deleteSearchAllItems(${JSON.stringify(allIds)})">删除所有</a>
                        </div>\`;
                    </td>
                `;
                tbody.appendChild(row);
            });

            resultContainer.appendChild(table);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function deleteSearchItem(id) {
    fetch(`/delete_search_data/${id}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(() => {
        searchData(); // 重新查询数据，刷新结果
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function deleteSearchAllItems(ids) {
    fetch('/delete_all_search_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ids: ids }),
    })
    .then(response => response.json())
    .then(() => {
        searchData(); // 重新查询数据，刷新结果
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function highlightKeyword(text, keyword) {
    if (!keyword) return text;
    try{
        const regex = new RegExp(`(${keyword})`, 'gi');
        text=text.replace(regex, '<span class="highlight">$1</span>');
    }catch (error){
        console.error('Error highlighting text:', error);
    }
    return text;
}


function replaceText() {
    const textInput1 = document.getElementById("textInput1").value;
    const textInput2 = document.getElementById("textInput2").value;

    if (textInput1 === '' || textInput2 === '') {
        alert('文本框1和文本框2不能为空');
        return;
    }

    fetch('/data_retrieval_replace', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text1: textInput1, text2: textInput2 }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        displayResults(data.results, textInput2);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function displayResults(data, textToHighlight) {
    const resultContainer = document.getElementById("resultContainer");
    resultContainer.innerHTML = ''; // 清空之前的结果

    if (data.length === 0) {
        resultContainer.innerHTML = '<div class="no-results">未查询到相关数据</div>';
    } else {
        const table = document.createElement("table");
        table.innerHTML = `
            <thead>
                <tr>
                    <th>序号</th>
                    <th>文本内容</th>
                    <th>修改结果</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;
        const tbody = table.querySelector("tbody");

        data.forEach((item, index) => {
            let highlightedText = item.text;
            if (textToHighlight) {
                const regex = new RegExp(textToHighlight, 'g');
                highlightedText = highlightedText.replace(regex, match => `<span style="background-color: red;">${match}</span>`);
            }
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${highlightedText}</td>
                <td>${item.result}</td>
            `;
            tbody.appendChild(row);
        });

        resultContainer.appendChild(table);
    }
}

