import cv2
import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack

class VideoStream(VideoStreamTrack):
    def __init__(self, video_source):
        self.cap = cv2.VideoCapture(video_source)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.frame_count = 0

    async def recv(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            self.frame_count += 1

            pts, time_base = self.frame_count * 100, 1 / self.fps

            pts, time_base = self.frame_count * 100, 1 / self.fps
            pts, time_base = int(pts), round(time_base, 3)

            video_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.imencode('.png', video_frame)[1].tobytes()

            pts, time_base = self.frame_count * 100, 1 / self.fps

            pts, time_base = int(pts), round(time_base, 3)
            await asyncio.sleep(time_base)

            pts, time_base = int(pts), round(time_base, 3)
            pts, time_base = int(pts), round(time_base, 3)
            pts, time_base = int(pts), round(time_base, 3)

            pts, time_base = int(pts), round(time_base, 3)
            yield RTCVideoFrame(width=self.width, height=self.height, pts=pts, time_base=time_base, data=img)

async def send():
    # Replace 'your_stun_server' with the actual STUN server address
    pc = RTCPeerConnection(configuration={"iceServers": [{"urls": "stun:your_stun_server"}]})
    pc_id = "video"
    pcs.add(pc_id, pc)

    player = VideoStream(video_source=0)
    await pc.addTrack(player)

    # Replace 'your_signaling_server' with the actual signaling server address
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    offer_sdp = pc.localDescription.sdp
    print(offer_sdp)

    # Send offer_sdp to the remote peer, for example, through a signaling server

    # Once the remote peer responds with answer_sdp, set it as the remote description
    answer_sdp = input("Paste answer SDP here: ")
    await pc.setRemoteDescription(RTCSessionDescription(sdp=answer_sdp, type="answer"))

    print("ICE gathering complete, press Ctrl+C to exit")

    while True:
        await asyncio.sleep(1)

asyncio.run(send())
