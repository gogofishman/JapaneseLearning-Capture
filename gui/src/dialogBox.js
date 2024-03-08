class DialogBox {
    /**
     * @private
     * @type {boolean}
     */
    sub_window_state = false

    display (text) {
        this.sub_window_state = !document.querySelector('.sub-window').classList.contains('state-none')
        document.querySelector('.sub-window').classList.remove('state-none')
        document.getElementById('dialogBox-container').classList.remove('state-none')

        document.getElementById('dialogBox-container-text').innerHTML = text
    }

    hidden () {
        if (this.sub_window_state) {
            document.querySelector('.sub-window').classList.remove('state-none')
        } else {
            document.querySelector('.sub-window').classList.add('state-none')
        }

        document.getElementById('dialogBox-container').classList.add('state-none')

        document.getElementById('dialogBox-container-text').innerHTML = ' '
    }
}

dialogBox = new DialogBox()