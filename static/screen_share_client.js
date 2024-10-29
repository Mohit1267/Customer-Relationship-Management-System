// static/screen_share_client.js
const startScreenShare = async (employeeId) => {
    const ws = new WebSocket(`ws://${window.location.host}/ws/screen_share/${employeeId}/`);

    ws.onopen = () => console.log("WebSocket connected for screen sharing");

    const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
    const [track] = stream.getVideoTracks();
    const peerConnection = new RTCPeerConnection();

    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            ws.send(JSON.stringify({ ice: event.candidate }));
        }
    };

    ws.onmessage = async (event) => {
        const data = JSON.parse(event.data);
        if (data.answer) {
            await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
        } else if (data.ice) {
            await peerConnection.addIceCandidate(new RTCIceCandidate(data.ice));
        }
    };

    peerConnection.addTrack(track, stream);
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    ws.send(JSON.stringify({ offer: offer }));
};

// Automatically start screen sharing for an employee
startScreenShare("employee123"); // Replace with dynamic employee ID
