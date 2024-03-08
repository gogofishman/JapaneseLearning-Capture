let table = document.getElementById('files-table')

class FileList {

    add (file_name, file_dict) {
        this[file_name] = {
            'path': file_dict.path,
            'size': file_dict.size,
            'jav_number': file_dict.jav_number,
            'uncensored': file_dict.uncensored,
            'subtitle': file_dict.subtitle,
            'long_jav_number': file_dict.long_jav_number,
            'ignore': false,
            'state': '等待',
        }

        //修改表格
        let row = document.createElement('tr')
        row.setAttribute('file-name', file_name)

        //番号可自行修改
        let jav_number_input = document.createElement('input')
        jav_number_input.setAttribute('type', 'text')
        jav_number_input.setAttribute('value', file_dict.jav_number ? file_dict.jav_number : '-')
        jav_number_input.setAttribute('file_name', file_name)
        jav_number_input.title = '解析后得到的番号，点击可自行修改'
        table.onchange = (event)=> {
            //修改番号同步到数据
            let file_name = event.target.getAttribute('file_name')
            this.change_jav_number(file_name, event.target.value)
        }

        //勾选框
        let checkbox = document.createElement('div')
        checkbox.classList.add('table-checkbox')
        checkbox.setAttribute('file_name', file_name)
        checkbox.innerHTML = `<svg class="table-checkbox-icon checkbox-selected" file_name="${file_name}" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"
                             width="100%" height="100%">
                            <path file_name="${file_name}" class="table-checkbox-icon-sub1"
                                  d="M725.725 527.476c0 122.054-98.994 221.050-221.050 221.050-122.054 0-220.941-98.994-220.941-221.050 0-122.054 98.887-221.050 220.941-221.050 122.054 0 221.050 98.994 221.050 221.050z"></path>
                            <path file_name="${file_name}" class="table-checkbox-icon-sub2" d="M504.721 121.757c-223.731 0-405.74 182.009-405.74 405.74s182.009 405.74 405.74 405.74c223.731 0 405.74-182.009 405.74-405.74 0-223.731-182.009-405.74-405.74-405.74M504.721 993.296c-98.243 0-189.516-30.567-264.807-82.8-85.909-59.525-150.903-147.259-181.579-249.793-12.656-42.257-19.412-86.981-19.412-133.206 0-78.403 19.412-152.3 53.733-217.187 34.428-64.887 83.658-120.767 143.184-163.025 75.935-53.948 168.816-85.589 268.884-85.589 83.013 0 161.095 21.772 228.665 60.062 85.482 48.37 154.337 123.019 195.309 212.897 26.919 58.775 41.828 124.094 41.828 192.839 0 91.595-26.599 177.183-72.503 249.363-42.686 67.141-102.107 122.591-172.247 160.558-65.853 35.609-141.145 55.879-221.050 55.879z"></path>
                        </svg>`
        table.onclick = (event) => {
            //判断点击的是checkbox按钮
            let classlist = event.target.classList
            if (!classlist.contains('table-checkbox-icon') &&
                !classlist.contains('table-checkbox-icon-sub1') &&
                !classlist.contains('table-checkbox-icon-sub2') &&
                !classlist.contains('table-checkbox')) return

            let file_name = event.target.getAttribute('file_name')
            let svg = document.querySelector(`svg[file_name="${file_name}"][class~="table-checkbox-icon"]`)
            let sub = document.querySelector(`path[file_name="${file_name}"][class~="table-checkbox-icon-sub1"]`)

            let value = this.toggle_jav_ignore(file_name) //获取改变后的状态

            if (!value) {
                //选中状态
                svg.classList.add('checkbox-selected')
                sub.classList.remove('state-hidden')
            } else {
                svg.classList.remove('checkbox-selected')
                sub.classList.add('state-hidden')
            }
        }

        row.innerHTML = `
            <td>${checkbox.outerHTML}</td>
            <td>${file_name}</td>
            <td>${Number(file_dict.size).toFixed(1)}</td>
            <td>${jav_number_input.outerHTML}</td>
            <td td-type="state">${this[file_name].state}</td>
        `
        table.appendChild(row)
    }

    change_jav_number (file_name, jav_number) {
        this[file_name].jav_number = jav_number
    }

    change_state (file_name, state) {
        this[file_name].state = state

        //修改表格
        let row = document.querySelector(`tr[file-name="${file_name}"]`)
        let td = row.querySelector('td[td-type="state"]')
        td.innerHTML = state
    }

    toggle_jav_ignore (file_name) {
        this[file_name].ignore = !this[file_name].ignore
        return this[file_name].ignore
    }

    remove (file_name) {
        delete this[file_name]

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

var file_list = new FileList()