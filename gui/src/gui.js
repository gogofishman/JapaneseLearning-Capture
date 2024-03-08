function init () {
    //改写右键
    document.addEventListener('contextmenu', function (event) {
        event.preventDefault()
    })

    //tab
    let tabs = document.querySelectorAll('.tab-icon-container')
    tabs.forEach((tab) => {
        tab.onclick = () => {
            tabs.forEach((tab) => {
                tab.classList.remove('selected')
            })
            tab.classList.add('selected')

            //tabView
            let connet = tab.getAttribute('connect')
            let tabViews = document.querySelectorAll('.main-container-tabView')
            tabViews.forEach((tabView) => {
                tabView.classList.add('state-none')
            })
            document.getElementById(connet).classList.remove('state-none')
        }
    })
    tabs[0].click()

    //开关控件
    let switchs = document.querySelectorAll('.switch')
    switchs.forEach((control) => {
        let connect = control.getAttribute('connect')
        pywebview.api[connect]().then((data) => {
            if (data) {
                control.classList.add('switch-on')
            } else {
                control.classList.remove('switch-on')
            }
        })

        control.onclick = () => {
            control.classList.toggle('switch-on')

            let value = control.classList.contains('switch-on')
            pywebview.api[connect](value)
        }
    })

    //combobox控件
    let comboboxs = document.querySelectorAll('.combobox')
    comboboxs.forEach((control) => {
        let connect = control.getAttribute('connect')
        pywebview.api[connect]().then((data) => {
            control.value = data
            control.text = data
        })

        control.onchange = () => {
            pywebview.api[connect](control.value)
        }
    })

    //数字输入控件
    let numberInputs = document.querySelectorAll('input[type="number"]')
    numberInputs.forEach((control) => {
        let connect = control.getAttribute('connect')
        if (!connect) return

        pywebview.api[connect]().then((data) => {
            data = Number(data)
            control.value = data
        })

        control.onchange = () => {
            pywebview.api[connect](Number(control.value))
        }

        control.onfocus = () => {
            control.select()
        }
    })

    //文本输入控件
    let textInputs = document.getElementById('main-setting').querySelectorAll('input[type="text"]')
    textInputs.forEach((control) => {
        let connect = control.getAttribute('connect')
        if (!connect) return

        pywebview.api[connect]().then((data) => {
            control.value = data
        })

        control.onchange = () => {
            pywebview.api[connect](control.value)
        }

        control.onfocus = () => {
            control.select()
        }
    })

    //初始化输入路径
    let inputPath = document.getElementById('input-path')
    pywebview.api.input_path().then((path) => {
        inputPath.value = path
    })
    inputPath.onchange = () => {
        pywebview.api.input_path(inputPath.value).then((path) => {
            inputPath.value = path
        })
    }
    inputPath.onfocus = () => {
        inputPath.select()
    }

    //刷新表格
    let refreshButton = document.getElementById('refresh-button')
    refreshButton.onclick = () => {
        file_list.clear()

        //获取文件字典
        pywebview.api.search_file().then((data) => {
            for (const file_name in data) {
                file_list.add(file_name, data[file_name])
            }
        })
    }

    //翻译配置按钮
    let trans_api_button = document.getElementById('trans-api-button')
    trans_api_button.onclick = () => {
        let engine = document.getElementById('combobox-translate-engine').value
        if (engine === 'google') {
            dialogBox.display('google翻译不需要额外配置自己的api')
            return
        }
        document.getElementById('translatr-api-response').value = ''

        document.querySelector('.sub-window').classList.remove('state-none')
        document.getElementById('translatr-api-container').classList.remove('state-none')

        //设置获取api指向的url
        let url_div = document.getElementById('translatr-api-url')
        if (engine === 'tencent'){
            url_div.href = 'https://cloud.tencent.com/product/tmt'
        }
        if (engine === 'baidu'){
            url_div.href = 'https://api.fanyi.baidu.com/product/11'
        }

        //读取id和key
        let id = ''
        let key = ''
        let get_id = async () => await pywebview.api[`translate_${engine}_id`]().then((data) => {
            id = data
        })
        let get_key = async () => await pywebview.api[`translate_${engine}_key`]().then((data) => {
            key = data
        })

        Promise.all([get_id(), get_key()])
            .then(results => {
                document.getElementById('translatr-api-id').value = id
                document.getElementById('translatr-api-key').value = key
            })
    }
    //翻译api确定按钮
    let trans_api_save = document.getElementById('translatr-api-save')
    trans_api_save.onclick = () => {
        let engine = document.getElementById('combobox-translate-engine').value
        let id = document.getElementById('translatr-api-id').value
        let key = document.getElementById('translatr-api-key').value

        pywebview.api[`translate_${engine}_id`](id)
        pywebview.api[`translate_${engine}_key`](key)

        document.querySelector('.sub-window').classList.add('state-none')
        document.getElementById('translatr-api-container').classList.add('state-none')
    }
    //翻译api测试按钮
    let trans_api_test = document.getElementById('translatr-api-test')
    trans_api_test.onclick = () => {
        let text = document.getElementById('translatr-api-text').value
        if (text === '') {
            return
        }

        let engine = document.getElementById('combobox-translate-engine').value
        let id = document.getElementById('translatr-api-id').value
        let key = document.getElementById('translatr-api-key').value

        pywebview.api[`translate_${engine}_id`](id)
        pywebview.api[`translate_${engine}_key`](key)

        pywebview.api.test_translate(text).then((data) => {
            document.getElementById('translatr-api-response').value = String(data)
        })
    }

    //开始刮削
    let runButton = document.getElementById('run-button')
    runButton.onclick = () => {
        for (const _file in file_list) {
            let file = file_list[_file]

            if (file.ignore) continue

            pywebview.api.scraper_run(file.jav_number).then((data) => {
                let state_text = ''
                switch (data) {
                    case 0:
                        state_text = '成功'
                        break
                    case -1:
                        state_text = '失败'
                        break
                    case 1:
                        state_text = '有误'
                        break
                }
                file_list.change_state(_file, state_text)
            })
        }
    }
}








