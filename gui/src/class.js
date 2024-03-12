let table = document.getElementById('file-table-body')

class FileTable {

    constructor () {
        this.scrape = ''
        this.file_list = {}
        this.item_list = {
            'selected': {
                'text-align': 'center',
                'width': '20px',
            },
            '番号': {
                'text-align': 'center',
                'width': '0.3',
            },
            '文件名': {
                'text-align': 'left',
                'width': '1',
            },
            '大小': {
                'text-align': 'left',
                'width': '60px',
            },
            '状态': {
                'text-align': 'left',
                'width': '120px',
            },
        }

        //表格初始化
        let table_head = document.getElementById('file-table-head')
        for (const item in this.item_list) {
            let div_item = document.createElement('div')
            div_item.classList.add('table-item')
            div_item.setAttribute('item', item)
            div_item.innerHTML = `<span>${item}</span>`

            table_head.appendChild(div_item)
        }
        this.update_table_style()

        //修改表格item显示内容
        for (const itemElement of table_head.children) {
            //selected
            if (itemElement.getAttribute('item') === 'selected') {
                itemElement.title = '全选'
                itemElement.innerHTML = `<input id="file-table-selectAll" type="checkbox" style="transform: translateY(5px)">`
                itemElement.children[0].onchange = () => {
                    document.getElementById('file-table-body')
                        .querySelectorAll('input[type="checkbox"]')
                        .forEach((checkbox) => {
                            if (itemElement.children[0].checked !== checkbox.checked) {
                                checkbox.click()
                            }
                        })
                }
            }
        }
    }

    add (file_name, file_dict) {
        //检查file_name是否唯一
        if (this.file_list[file_name] !== undefined) return

        this.file_list[file_name] = {
            'path': file_dict.path,
            'size': file_dict.size,
            'jav_number': file_dict.jav_number,
            'uncensored': file_dict.uncensored,
            'subtitle': file_dict.subtitle,
            'long_jav_number': file_dict.long_jav_number,
            'selected': false,
            'state': '等待',
        }

        //在表格中新增一行
        let div_line = document.createElement('div')
        div_line.classList.add('table-line')
        div_line.setAttribute('file', file_name)

        //添加item
        div_line.innerHTML = `  <div class="table-item" item="selected"><input type="checkbox" onchange="file_table.change_file_selected('${file_name}',this.checked)"></div>
                                <div class="table-item state-selectable-text" item="番号">
                                    <input type="text" title="如果番号解析有误，可自行修改" value="${this.file_list[file_name]['jav_number']}" onchange="file_table.change_jav_number('${file_name}',this.value)">
                                </div>
                                <div class="table-item state-selectable-text" item="文件名"><span>${file_name}</span></div>
                                <div class="table-item" item="大小"><span>${this.file_list[file_name]['size']} GB</span></div>
                                <div class="table-item" item="状态"><span>${this.file_list[file_name]['state']}</span></div>  `

        table.appendChild(div_line)

        this.update_table_style()

        //默认选中
        div_line.children[0].children[0].click()
    }

    /**
     * 更新表格的style
     * @private
     */
    update_table_style () {
        let lines = [document.getElementById('file-table-head'), ...document.getElementById('file-table-body').children]
        lines.forEach((line) => {
            for (const item of line.children) {
                //对齐方式
                switch (this.item_list[item.getAttribute('item')]['text-align']) {
                    case 'center':
                        item.style.justifyContent = 'center'
                        break
                    case 'left':
                        item.style.justifyContent = 'flex-start'
                        break
                    case 'right':
                        item.style.justifyContent = 'flex-end'
                        break
                    default:
                        item.style.justifyContent = 'flex-start'
                        break
                }

                //宽度
                if (this.item_list[item.getAttribute('item')]['width'].includes('px')) {
                    item.style.width = this.item_list[item.getAttribute('item')]['width']
                } else {
                    item.style.flex = this.item_list[item.getAttribute('item')]['width']
                }
            }
        })

        //滚动条出现则head添加10px右padding
        if (table.scrollHeight > table.clientHeight) {
            table.style.paddingRight = '10px'
        }
    }

    change_jav_number (file_name, jav_number) {
        this.file_list[file_name].jav_number = jav_number
    }

    change_state (file_name, state) {
        this.file_list[file_name].state = state

        //修改表格
        document.getElementById('file-table-body')
            .querySelector('div[file="' + file_name + '"]')
            .querySelector('div[item="状态"]')
            .children[0].innerHTML = state
    }

    change_file_selected (file_name, value) {
        this.file_list[file_name]['selected'] = value
        return this.file_list[file_name].selected
    }

    remove (file_name) {
        delete this.file_list[file_name]

        //修改表格
        let line = document.getElementById('file-table-body')
            .querySelector(`div[file="${file_name}"]`)
        line.remove()
    }

    clear () {
        for (const file_name in this.file_list) {
            this.remove(file_name)
        }
    }
}

class ProgressBar {
    constructor () {
        this._num = 0
        this._total = 0
        this._div_label = document.getElementById('progress-bar-label')
        this._div_percent_text = document.getElementById('progress-bar-percent')
        this._div_progress_bar = document.getElementById('scrape-progress-bar')
    }

    /**
     * 初始化
     * @param label{string} 标签
     * @param total{number} 进度总数
     */
    init (label, total) {
        this._num = 0
        this._total = total
        this.change_label(label)
        this.change_percent(`${this._num}/${this._total}`)
        this.change_bar(this._num, this._total)
    }

    /**
     * 更新进度
     * @param label{string|null} 改变标签，如果null则不改变
     * @param step{number} 进度前进的步数，默认为1
     */
    update (label = null, step = 1) {
        this._num = this._num + step
        this._num = this._total < this._num ? this._total : this._num
        if (label) this.change_label(label)
        this.change_percent(`${this._num}/${this._total}`)
        this.change_bar(this._num, this._total)
    }

    /**
     * @private
     */
    change_label (text) {
        this._div_label.innerText = text
    }

    /**
     * @private
     */
    change_percent (text) {
        this._div_percent_text.innerText = text
    }

    /**
     * @private
     */
    change_bar (num, total) {
        this._div_progress_bar.style.width = `${(num / total) * 100}%`
    }
}

var file_table = new FileTable()
var progress_bar = new ProgressBar()

