import c4d
from c4d import gui


def main():

    fps_doc = doc[c4d.DOCUMENT_FPS]
    fps_slow = 8
    skipped_fps_rate = fps_doc // fps_slow

    originalobj = doc.GetActiveObject()
    if not originalobj:
        return False
    init_iterator(originalobj, fps_doc, skipped_fps_rate)


# so script will effect reccursively every object of the hierqrchy.
def init_iterator(originalobj, fps_doc, skipped_fps_rate):

    sampleObject(originalobj, fps_doc, skipped_fps_rate)
    iterator(originalobj.GetDown(), fps_doc, skipped_fps_rate)


def iterator(obj, fps_doc, skipped_fps_rate):

    if not obj:
        return
    sampleObject(obj, fps_doc, skipped_fps_rate)
    iterator(obj.GetDown(), fps_doc, skipped_fps_rate)
    iterator(obj.GetNext(), fps_doc, skipped_fps_rate)


# return the first and last fps of the animation that shall be modified.
# frames returned are int (based on the document frame rate)m not C4D Frame object.
def getStartEndFrame(obj, fps_doc):

    startFrame = -1
    endFrame = -1
    for track in obj.GetCTracks():
        curve = track.GetCurve()
        s_tmp = curve.GetStartTime().GetFrame(fps_doc)
        e_tmp = curve.GetEndTime().GetFrame(fps_doc)
        if startFrame > s_tmp or startFrame == -1:
            startFrame = s_tmp
        if endFrame < e_tmp or endFrame == -1:
            endFrame = e_tmp
    return startFrame, endFrame


# Sample a given object by skipping a skipped_fps_rate number of frame.
def sampleObject(obj, fps_doc, skipped_fps_rate):

    obj.SetBit(c4d.BIT_ACTIVE)
    trk = obj.GetFirstCTrack()
    if not trk:
        return False
    startFrame, endFrame = getStartEndFrame(obj, fps_doc)

    # Registering every values of every tracks, before any processing is done 
    # so it doesn t alter the animation.
    keyFrameValueDict = {}
    for track in obj.GetCTracks():
        keyFrameValueDict[str(track.GetDescriptionID())] = {}
    for currentFps in range(startFrame, endFrame+1):
        if currentFps % skipped_fps_rate == 0 :
            baseTime_FPS = c4d.BaseTime(currentFps, fps_doc)
            doc.SetTime(baseTime_FPS)
            for track in obj.GetCTracks():
                valueToAdd = track.GetCurve().GetValue(baseTime_FPS)
                keyFrameValueDict[str(track.GetDescriptionID())][currentFps]= valueToAdd

    # Adding all necessary keys
    for currentFps in range(startFrame, endFrame + 1):
        if currentFps % skipped_fps_rate == 0:
            baseTime_FPS = c4d.BaseTime(currentFps, fps_doc)
            doc.SetTime(baseTime_FPS)
            c4d.EventAdd()
            # ask to redraw the view
            c4d.DrawViews(c4d.DRAWFLAGS_FORCEFULLREDRAW)
            # send message to c4d we have change the time
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            doc.ExecutePasses(None, True, True, True, 0)
            obj.Message(c4d.MSG_UPDATE)
            c4d.CallCommand(12410)

    # modifying the interpolation method of every frame just created.
    for track in obj.GetCTracks():
        curve = track.GetCurve()
        cnt = curve.GetKeyCount()
        for i in xrange(cnt):
            key = curve.GetKey(i)
            key.SetInterpolation(curve, 3)

    #Setting the  key values with the data registered earlier.
    for currentFps in range(startFrame, endFrame + 1):
        baseTime_FPS = c4d.BaseTime(currentFps, fps_doc)
        if currentFps % skipped_fps_rate == 0:
            for track in obj.GetCTracks():
                curve = track.GetCurve()
                key = curve.FindKey(baseTime_FPS)['key']
                key.SetValue(curve, keyFrameValueDict[str(track.GetDescriptionID())][currentFps])

    obj.DelBit(c4d.BIT_ACTIVE)
    return True


if __name__ == '__main__':
    main()
