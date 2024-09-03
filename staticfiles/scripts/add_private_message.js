document.addEventListener('DOMContentLoaded', () => {
	const roomName = JSON.parse(document.getElementById('room-name').textContent);
	var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	const chatSocket = new WebSocket(
		`${ws_scheme}://`
		+ window.location.host
		+ '/ws/chat/'
		+ roomName
		+ '/'
	);

	chatSocket.onmessage = function (e) {
		let data = JSON.parse(e.data);
		const chatLog = document.querySelector('#chat-log');
		let messageElement = document.createElement('div');
		messageElement.classList.add("mt-3", 'p-4', "w-full", "flex", 'items-start', 'rounded-md', 'bg-white'); 
		messageElement.innerHTML = `
			<div class="pic w-12 aspect-square rounded-full overflow-hidden">
				<img src="${data.sender_img}" alt="頭貼" class="block w-full h-full object-cover">
			</div>
			<div class="ml-2 flex-1 break-all">
				<p class="text-xl">${data.sender_name} <span class="text-xs">${data.created_at}</span></p>
				<p class="w-full">${data.content}</p>						
			</div>
		`
		chatLog.appendChild(messageElement);
		chatLog.scrollTop = chatLog.scrollHeight;
	};

	chatSocket.onclose = function (e) {
		console.error('Chat socket closed unexpectedly');
	};

	const messageInputDom = document.querySelector('#chat-message-input');
	const messageSubmitDom = document.querySelector('#chat-message-submit');
	messageInputDom.focus();
	

	messageInputDom.addEventListener("input", function() {
		if (messageInputDom.value.trim() != "") {
			messageSubmitDom.removeAttribute("disabled");
		} else {
			messageSubmitDom.setAttribute("disabled", "disabled");
		}
	})
	
	messageInputDom.onkeyup = function (e) {
		if (e.key === 'Enter') {
			messageSubmitDom.click();
		}
	};

	messageSubmitDom.onclick = function (e) {
		const userId = document.querySelector("#chat-message-user").dataset.userId;
		const userName = document.querySelector('#chat-message-user').dataset.userName;
		const userImg = document.querySelector('#chat-message-user').dataset.userImg;
		const message = messageInputDom.value.trim()

		const privateUsers = roomName.split("_");
		const receiverId = privateUsers[0] == userId ? privateUsers[1] : privateUsers[0];
		chatSocket.send(JSON.stringify({
			"senderId": userId,
			"receiverId": receiverId,
			"message": message,
			"senderName": userName,
			"senderImg": userImg,
		}));
		messageInputDom.value = '';
		messageSubmitDom.setAttribute("disabled", "disabled");
	};
})