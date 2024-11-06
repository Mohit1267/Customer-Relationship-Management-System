// static/screen_share_admin.js
const viewEmployeeScreen = (employeeId) => {
    const ws = new WebSocket(`ws://${window.location.host}/ws/screen_share/${employeeId}/`);
    const peerConnection = new RTCPeerConnection();

    ws.onopen = () => console.log("Connected to WebSocket for viewing employee screen");

    ws.onmessage = async (event) => {
        const data = JSON.parse(event.data);
        if (data.offer) {
            await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
            const answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);
            ws.send(JSON.stringify({ answer: answer }));
        } else if (data.ice) {
            await peerConnection.addIceCandidate(new RTCIceCandidate(data.ice));
        }
    };

    peerConnection.ontrack = (event) => {
        const videoElement = document.getElementById("employee-video");
        videoElement.srcObject = event.streams[0];
    };
};

// Function call for viewing employee screen - replace "employee123" dynamically based on selection
viewEmployeeScreen("employee123");
