var resize_mousedown = false
var resize_direction = null

function window_event_init () {
    //右上角最小化关闭按钮事件
    document.getElementById('minimize-button').onclick = () => {
        pywebview.api.window_minimize()
    }
    document.getElementById('maximize-button').onclick = () => {
        pywebview.api.window_maximize()
    }
    document.getElementById('close-button').onclick = () => {
        pywebview.api.window_close()
    }

    //窗口大小调整
    document.onmouseup = (event) => {
        resize_mousedown = false
    }
    document.onmousemove = (event) => {
        if (!resize_mousedown) return
        pywebview.api.window_resize_update(resize_direction)
    }

    let resize_bars = document.getElementsByClassName('resize-bar')
    for (const resizeBar of resize_bars) {
        resizeBar.onmousedown = (event) => {
            resize_mousedown = true
            resize_direction = resizeBar.id.substring(11);
            pywebview.api.window_resize_start()
        }
    }
}