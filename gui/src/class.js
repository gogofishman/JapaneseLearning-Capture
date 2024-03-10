let table = document.getElementById('file-table-body')

class FileTable {

    constructor () {
        this.file_list = {}
        this.scraper_global = 'JavDB'
        this.item_list = {
            'selected': {
                'text-align': 'center',
                'width': '20px',
            },
            '刮削器': {
                'text-align': 'center',
                'width': '70px',
            },
            '番号': {
                'text-align': 'center',
                'width': '0.4',
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
                'width': '60px',
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
                        .forEach((checkbox) => {checkbox.click()})
                }
            }
        }
    }

    add (file_name, file_dict) {
        //检查file_name是否唯一
        // if (this.file_list[file_name] !== undefined) return

        this.file_list[file_name] = {
            'scraper': this.scraper_global,
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
                                <div class="table-item" item="刮削器"><span>${this.file_list[file_name]['scraper']}</span></div>
                                <div class="table-item state-selectable-text" item="番号"><span>${this.file_list[file_name]['jav_number']}</span></div>
                                <div class="table-item state-selectable-text" item="文件名"><span>${file_name}</span></div>
                                <div class="table-item" item="大小"><span>${this.file_list[file_name]['size']} GB</span></div>
                                <div class="table-item" item="状态"><span>${this.file_list[file_name]['state']}</span></div>  `

        table.appendChild(div_line)

        this.update_table_style()
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
        let row = document.querySelector(`tr[file-name="${file_name}"]`)
        let td = row.querySelector('td[td-type="state"]')
        td.innerHTML = state
    }

    change_file_selected (file_name, value) {
        this.file_list[file_name]['selected'] = value
        return this.file_list[file_name].selected
    }

    remove (file_name) {
        delete this.file_list[file_name]

        //修改表格
        let row = document.querySelector(`tr[file-name="${file_name}"]`)
        table.removeChild(row)
    }

    clear () {
        for (const file_name in this) {
            this.remove(file_name)
        }
    }
}

var file_table = new FileTable()

file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})
file_table.add('hhd800.com@GVH-624.mp4', {
    'path': 'hhd800.com@GVH-624.mp4',
    'size': '6.2',
    'jav_number': 'GVH-624',
    'uncensored': false,
    'subtitle': false,
    'long_jav_number': 'GVH-624'
})


