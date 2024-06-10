const roomNameInputs = document.querySelectorAll(".room-name-input")
const roomNameSubmits = document.querySelectorAll(".room-name-submit")
    roomNameSubmits.forEach((submitButton, index) => {
        submitButton.addEventListener("click", function() {
        const roomName = roomNameInputs[index].value.split(',').sort((a, b) => (a - b))
        const newRoomName = roomName[0] + "_" + roomName[1]
        window.location.pathname = '/chat/' + newRoomName + '/';
        })
})
