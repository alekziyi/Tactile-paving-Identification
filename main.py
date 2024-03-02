import cv2
import asyncio
from aiortc import MediaStreamTrack, RTCPeerConnection, VideoStreamTrack


class VideoStream(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame = None

    async def recv(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.timestamp += 1
            await asyncio.sleep(0.01)  # 控制帧率

    def close(self):
        self.cap.release()


async def offer(pc, video_track):
    params = {"audio": False, "video": True}
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    params["sdp"] = pc.localDescription.sdp

    # 发送 offer 给另一端，对端需在 answer 中设置远程描述
    return params


async def answer(pc, offer, video_track):
    await pc.setRemoteDescription(RTCSessionDescription(sdp=offer["sdp"], type="offer"))
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    # 发送 answer 给发起方，对方需设置为本地描述
    return {"sdp": pc.localDescription.sdp, "type": "answer"}


async def consume_answer(pc, answer):
    # 设置远程描述
    await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type="answer"))


async def consume_ice(pc, ice):
    # 添加远程候选
    candidate = RTCIceCandidate(sdp=ice["candidate"], sdp_mid=ice["sdpMid"], sdp_mline_index=ice["sdpMLineIndex"])
    await pc.addIceCandidate(candidate)


async def run(pc, video_track):
    done = asyncio.Event()

    async def close():
        await video_track.stop()
        await pc.close()
        done.set()

    # 处理关闭事件
    pc.oniceconnectionstatechange = lambda x: close()
    pc.onicegatheringstatechange = lambda x: close()
    pc.onsignalingstatechange = lambda x: close()

    # 本地 SDP Offer
    params = await offer(pc, video_track)

    # 处理 Answer
    answer_params = await answer(pc, params, video_track)

    # 处理远程描述和 ICE 候选
    await consume_answer(pc, answer_params)
    await consume_ice(pc, {"candidate": "", "sdpMid": "", "sdpMLineIndex": 0})

    # 等待关闭事件发生
    await done.wait()


async def main():
    pc = RTCPeerConnection()
    video_track = VideoStream()

    pc_id = pc.sctp.transport.transport_id
    consumers = {}

    @pc.on("datachannel")
    def on_datachannel(channel):
        consumers[channel.channel_id] = channel

    # 启动视频流
    video_task = asyncio.ensure_future(video_track.recv())

    # 运行 WebRTC
    await asyncio.gather(run(pc, video_track), video_task)


if __name__ == "__main__":
    asyncio.run(main())
