import pandas as pd
import json
from pathlib import Path

def csv_to_json(df):
    result = {}
    current_path = []
    
    for _, row in df.iterrows():
        # 跳過標題行
        if row['JSON Format'] == 'JSON Format':
            continue
            
        # 處理縮進級別
        indent_level = 0
        for col in df.columns[:10]:  # 增加檢查的列數以確保能正確識別縮進
            if pd.isna(row[col]):
                indent_level += 1
            else:
                break
        
        # 獲取當前行的值
        values = row[~pd.isna(row)].values
        if len(values) == 0:
            continue
            
        node_name = values[0]
        
        # 根據縮進級別更新路徑
        current_path = current_path[:indent_level]
        current_path.append(node_name)
        
        # 創建或更新節點
        current = result
        for i, path in enumerate(current_path[:-1]):
            if path not in current:
                current[path] = {}
            current = current[path]
        
        # 添加當前節點
        if current_path[-1] not in current:
            current[current_path[-1]] = {}
            
        node = current[current_path[-1]]
        if isinstance(node, str):
            node = {}
            current[current_path[-1]] = node
        
        # 添加屬性
        if 'Data Type' in row.index and pd.notna(row['Data Type']):
            node['type'] = row['Data Type']
        if 'Default Value' in row.index and pd.notna(row['Default Value']):
            node['default'] = row['Default Value']
        if 'parameter limit' in row.index and pd.notna(row['parameter limit']):
            node['limit'] = row['parameter limit']
        if 'Comment' in row.index and pd.notna(row['Comment']):
            node['comment'] = row['Comment']
    
    return result

def create_html(json_data):
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>CSV to JSON Viewer</title>
        <style>
            :root {
                --primary-color: #3b82f6;
                --secondary-color: #64748b;
                --success-color: #10b981;
                --warning-color: #f59e0b;
                --text-color: #1e293b;
                --bg-color: #f8fafc;
                --container-bg: #ffffff;
                --hover-bg: #f1f5f9;
                --border-color: #e2e8f0;
                --shadow-color: rgba(0, 0, 0, 0.05);
                --level-1-color: #3b82f6;
                --level-2-color: #8b5cf6;
                --level-3-color: #ec4899;
                --level-4-color: #f97316;
                --level-5-color: #10b981;
                --level-6-color: #06b6d4;
                --level-7-color: #d946ef;
                --level-8-color: #f43f5e;
                --level-9-color: #84cc16;
                --level-10-color: #6366f1;
                --comment-color: #f59e0b;
            }

            [data-theme="dark"] {
                --primary-color: #60a5fa;
                --secondary-color: #94a3b8;
                --success-color: #34d399;
                --warning-color: #fbbf24;
                --text-color: #f1f5f9;
                --bg-color: #0f172a;
                --container-bg: #1e293b;
                --hover-bg: #334155;
                --border-color: #475569;
                --shadow-color: rgba(0, 0, 0, 0.2);
                --level-1-color: #60a5fa;
                --level-2-color: #a78bfa;
                --level-3-color: #f472b6;
                --level-4-color: #fb923c;
                --level-5-color: #34d399;
                --level-6-color: #22d3ee;
                --level-7-color: #e879f9;
                --level-8-color: #fb7185;
                --level-9-color: #a3e635;
                --level-10-color: #818cf8;
                --comment-color: #fbbf24;
            }

            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 20px;
                background-color: var(--bg-color);
                color: var(--text-color);
                transition: all 0.3s ease;
            }

            .theme-switch {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 8px 16px;
                background-color: var(--container-bg);
                border: 1px solid var(--border-color);
                border-radius: 20px;
                cursor: pointer;
                font-size: 0.9em;
                color: var(--text-color);
                transition: all 0.3s ease;
                box-shadow: 0 2px 4px var(--shadow-color);
            }

            .theme-switch:hover {
                background-color: var(--hover-bg);
                transform: translateY(-1px);
            }

            .json-container {
                background-color: var(--container-bg);
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 8px 16px var(--shadow-color);
                max-width: 1200px;
                margin: 0 auto;
                transition: all 0.3s ease;
                margin-top: 60px;
            }

            .json-node {
                margin-left: 20px;
                position: relative;
                transition: all 0.3s ease;
            }

            .json-key {
                color: var(--primary-color);
                font-weight: 600;
                font-size: 1.05em;
                transition: all 0.2s ease;
            }

            .json-value {
                color: var(--text-color);
            }

            .json-type {
                color: var(--secondary-color);
                font-style: italic;
                font-size: 0.9em;
                margin-left: 5px;
                opacity: 0.9;
            }

            .json-default {
                color: var(--success-color);
                font-weight: 500;
            }

            .json-limit {
                color: var(--warning-color);
                font-weight: 500;
            }

            .json-comment {
                color: var(--comment-color);
                font-style: italic;
                font-size: 0.9em;
                opacity: 0.9;
            }

            .toggle {
                cursor: pointer;
                color: var(--secondary-color);
                display: inline-block;
                width: 20px;
                height: 20px;
                text-align: center;
                line-height: 20px;
                background-color: var(--hover-bg);
                border-radius: 50%;
                margin-right: 8px;
                transition: all 0.2s ease;
                font-size: 0.8em;
                box-shadow: 0 1px 2px var(--shadow-color);
            }

            .toggle:hover {
                background-color: var(--primary-color);
                color: white;
                transform: scale(1.1);
            }

            .collapsed > .json-children {
                display: none;
            }

            .property-line {
                margin: 8px 0;
                padding: 8px 12px;
                border-radius: 8px;
                transition: all 0.2s ease;
                position: relative;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .property-line:hover {
                background-color: var(--hover-bg);
                box-shadow: 0 2px 4px var(--shadow-color);
                transform: translateX(4px);
            }

            .property-content {
                display: flex;
                align-items: center;
                flex-wrap: wrap;
                gap: 8px;
            }

            .json-comment {
                color: var(--comment-color);
                font-style: italic;
                font-size: 0.9em;
                opacity: 0.9;
                margin-left: auto;
                padding-left: 20px;
            }

            h1 {
                color: var(--text-color);
                text-align: center;
                margin-bottom: 30px;
                font-weight: 600;
                font-size: 2.2em;
                text-shadow: 1px 1px 2px var(--shadow-color);
                position: relative;
                padding-bottom: 10px;
            }

            h1::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 100px;
                height: 3px;
                background: var(--primary-color);
                border-radius: 3px;
                box-shadow: 0 1px 2px var(--shadow-color);
            }

            .json-children {
                border-left: 2px solid var(--border-color);
                margin-left: 10px;
                padding-left: 15px;
                transition: all 0.3s ease;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .json-node {
                animation: fadeIn 0.3s ease-out;
            }

            .json-key.level-1 {
                color: var(--level-1-color);
            }

            .json-key.level-2 {
                color: var(--level-2-color);
            }

            .json-key.level-3 {
                color: var(--level-3-color);
            }

            .json-key.level-4 {
                color: var(--level-4-color);
            }

            .json-key.level-5 {
                color: var(--level-5-color);
            }

            .json-key.level-6 {
                color: var(--level-6-color);
            }

            .json-key.level-7 {
                color: var(--level-7-color);
            }

            .json-key.level-8 {
                color: var(--level-8-color);
            }

            .json-key.level-9 {
                color: var(--level-9-color);
            }

            .json-key.level-10 {
                color: var(--level-10-color);
            }

            .control-buttons {
                position: fixed;
                top: 20px;
                right: 20px;
                display: flex;
                gap: 10px;
                z-index: 1000;
                background-color: var(--container-bg);
                padding: 10px;
                border-radius: 20px;
                box-shadow: 0 4px 6px var(--shadow-color);
            }

            .control-button {
                padding: 8px 16px;
                background-color: var(--container-bg);
                border: 1px solid var(--border-color);
                border-radius: 20px;
                cursor: pointer;
                font-size: 0.9em;
                color: var(--text-color);
                transition: all 0.3s ease;
                box-shadow: 0 2px 4px var(--shadow-color);
                z-index: 1001;
            }

            .control-button:hover {
                background-color: var(--hover-bg);
                transform: translateY(-1px);
            }
        </style>
    </head>
    <body>
        <div class="control-buttons">
            <button class="control-button" onclick="toggleTheme()">切换主题</button>
            <button class="control-button" onclick="expandAll()">展开全部</button>
            <button class="control-button" onclick="collapseAll()">折叠全部</button>
        </div>
        <h1>csv to json to HTML</h1>
        <div class="json-container">
            <div id="json-viewer"></div>
        </div>
        <script>
            // 等待 DOM 加载完成
            document.addEventListener('DOMContentLoaded', function() {
                const jsonData = {json_data};
                createJsonViewer(jsonData, document.getElementById('json-viewer'));
            });

            function toggleTheme() {
                const body = document.body;
                const currentTheme = body.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                body.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
            }

            function expandAll() {
                const nodes = document.querySelectorAll('.json-node');
                nodes.forEach(node => {
                    if (node.querySelector('.toggle')) {
                        node.classList.remove('collapsed');
                        const toggle = node.querySelector('.toggle');
                        toggle.innerHTML = '&#9660;';
                    }
                });
            }

            function collapseAll() {
                const nodes = document.querySelectorAll('.json-node');
                nodes.forEach(node => {
                    if (node.querySelector('.toggle')) {
                        node.classList.add('collapsed');
                        const toggle = node.querySelector('.toggle');
                        toggle.innerHTML = '&#9654;';
                    }
                });
            }

            // 初始化主题
            const savedTheme = localStorage.getItem('theme') || 'light';
            document.body.setAttribute('data-theme', savedTheme);

            function createJsonViewer(data, container, level = 1) {
                if (typeof data !== 'object' || data === null) {
                    return;
                }

                const node = document.createElement('div');
                node.className = 'json-node';
                
                const propertyLine = document.createElement('div');
                propertyLine.className = 'property-line';
                
                const propertyContent = document.createElement('div');
                propertyContent.className = 'property-content';
                
                const keys = Object.keys(data);
                if (keys.length === 0) {
                    return;
                }
                
                const firstKey = keys[0];
                const value = data[firstKey];
                
                // 检查是否有子节点需要折叠
                let hasChildren = false;
                for (const [k, v] of Object.entries(value)) {
                    if (k !== 'type' && k !== 'default' && k !== 'limit' && k !== 'comment' && 
                        typeof v === 'object' && v !== null) {
                        hasChildren = true;
                        break;
                    }
                }

                if (hasChildren) {
                    const toggle = document.createElement('span');
                    toggle.className = 'toggle';
                    toggle.innerHTML = '&#9660;';
                    toggle.onclick = function() {
                        node.classList.toggle('collapsed');
                        this.innerHTML = node.classList.contains('collapsed') ? '&#9654;' : '&#9660;';
                    };
                    propertyContent.appendChild(toggle);
                }
                
                const key = document.createElement('span');
                key.className = `json-key level-${Math.min(level, 10)}`;
                
                const children = document.createElement('div');
                children.className = 'json-children';
                
                if (value && typeof value === 'object' && 'type' in value) {
                    key.textContent = firstKey + ' ';
                    const type = document.createElement('span');
                    type.className = 'json-type';
                    type.textContent = `(${value.type})`;
                    propertyContent.appendChild(key);
                    propertyContent.appendChild(type);
                    
                    if (value.default) {
                        const defaultValue = document.createElement('span');
                        defaultValue.className = 'json-default';
                        defaultValue.textContent = ` = ${value.default}`;
                        propertyContent.appendChild(defaultValue);
                    }
                    
                    if (value.limit) {
                        const limit = document.createElement('span');
                        limit.className = 'json-limit';
                        limit.textContent = ` [${value.limit}]`;
                        propertyContent.appendChild(limit);
                    }
                    
                    propertyLine.appendChild(propertyContent);
                    
                    if (value.comment) {
                        const comment = document.createElement('span');
                        comment.className = 'json-comment';
                        comment.textContent = `// ${value.comment}`;
                        propertyLine.appendChild(comment);
                    }
                    
                    node.appendChild(propertyLine);
                    node.appendChild(children);
                    
                    // 处理子节点
                    for (const [k, v] of Object.entries(value)) {
                        if (k !== 'type' && k !== 'default' && k !== 'limit' && k !== 'comment') {
                            if (typeof v === 'object' && v !== null) {
                                const childData = {};
                                childData[k] = v;
                                createJsonViewer(childData, children, level + 1);
                            }
                        }
                    }
                } else if (typeof value === 'object' && value !== null) {
                    key.textContent = firstKey;
                    propertyContent.appendChild(key);
                    
                    propertyLine.appendChild(propertyContent);
                    node.appendChild(propertyLine);
                    node.appendChild(children);
                    
                    // 处理子节点
                    for (const [k, v] of Object.entries(value)) {
                        if (typeof v === 'object' && v !== null) {
                            const childData = {};
                            childData[k] = v;
                            createJsonViewer(childData, children, level + 1);
                        }
                    }
                }
                
                container.appendChild(node);
            }
        </script>
    </body>
    </html>
    """
    return html_template.replace('{json_data}', json.dumps(json_data))

def main():
    # 讀取 CSV 文件
    df = pd.read_csv('./data.csv')
    
    # 轉換為 JSON
    json_data = csv_to_json(df)
    
    # 創建 HTML
    html_content = create_html(json_data)
    
    # 保存 HTML 文件
    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML 文件已生成：output.html")

if __name__ == "__main__":
    main() 