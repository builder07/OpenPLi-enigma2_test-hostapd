from enigma import eDVBResourceManager, Misc_Options, eDVBCIInterfaces, eGetEnigmaDebugLvl
from Tools.Directories import fileExists, fileCheck, pathExists, fileHas
from Tools.HardwareInfo import HardwareInfo

import os

SystemInfo = {}

def getNumVideoDecoders():
	number_of_video_decoders = 0
	while fileExists("/dev/dvb/adapter0/video%d" % (number_of_video_decoders), 'f'):
		number_of_video_decoders += 1
	return number_of_video_decoders

def countFrontpanelLEDs():
	number_of_leds = fileExists("/proc/stb/fp/led_set_pattern") and 1 or 0
	while fileExists("/proc/stb/fp/led%d_pattern" % number_of_leds):
		number_of_leds += 1
	return number_of_leds

def hassoftcaminstalled():
	from Tools.camcontrol import CamControl
	return len(CamControl('softcam').getList()) > 1

SystemInfo["InDebugMode"] = eGetEnigmaDebugLvl() >= 4
SystemInfo["CommonInterface"] = eDVBCIInterfaces.getInstance().getNumOfSlots()
SystemInfo["CommonInterfaceCIDelay"] = fileCheck("/proc/stb/tsmux/rmx_delay")
for cislot in range (0, SystemInfo["CommonInterface"]):
	SystemInfo["CI%dSupportsHighBitrates" % cislot] = fileCheck("/proc/stb/tsmux/ci%d_tsclk"  % cislot)
	SystemInfo["CI%dRelevantPidsRoutingSupport" % cislot] = fileCheck("/proc/stb/tsmux/ci%d_relevant_pids_routing"  % cislot)

SystemInfo["HasSoftcamInstalled"] = hassoftcaminstalled()
SystemInfo["NumVideoDecoders"] = getNumVideoDecoders()
SystemInfo["PIPAvailable"] = SystemInfo["NumVideoDecoders"] > 1
SystemInfo["CanMeasureFrontendInputPower"] = eDVBResourceManager.getInstance().canMeasureFrontendInputPower()
SystemInfo["12V_Output"] = Misc_Options.getInstance().detected_12V_output()
SystemInfo["ZapMode"] = fileCheck("/proc/stb/video/zapmode") or fileCheck("/proc/stb/video/zapping_mode")
SystemInfo["NumFrontpanelLEDs"] = countFrontpanelLEDs()
SystemInfo["FrontpanelDisplay"] = fileExists("/dev/dbox/oled0") or fileExists("/dev/dbox/lcd0")
SystemInfo["LCDsymbol_circle_recording"] = fileCheck("/proc/stb/lcd/symbol_circle") or HardwareInfo().get_device_model() in ("hd51", "vs1500") and fileCheck("/proc/stb/lcd/symbol_recording")
SystemInfo["LCDsymbol_timeshift"] = fileCheck("/proc/stb/lcd/symbol_timeshift")
SystemInfo["LCDshow_symbols"] = (HardwareInfo().get_device_model().startswith("et9") or HardwareInfo().get_device_model() in ("hd51", "vs1500")) and fileCheck("/proc/stb/lcd/show_symbols")
SystemInfo["LCDsymbol_hdd"] = HardwareInfo().get_device_model() in ("hd51", "vs1500") and fileCheck("/proc/stb/lcd/symbol_hdd")
SystemInfo["FrontpanelDisplayGrayscale"] = fileExists("/dev/dbox/oled0")
SystemInfo["DeepstandbySupport"] = HardwareInfo().get_device_name() != "dm800"
SystemInfo["Fan"] = fileCheck("/proc/stb/fp/fan")
SystemInfo["FanPWM"] = SystemInfo["Fan"] and fileCheck("/proc/stb/fp/fan_pwm")
SystemInfo["PowerLED"] = fileCheck("/proc/stb/power/powerled")
SystemInfo["StandbyLED"] = fileCheck("/proc/stb/power/standbyled")
SystemInfo["SuspendLED"] = fileCheck("/proc/stb/power/suspendled")
SystemInfo["Display"] = SystemInfo["FrontpanelDisplay"] or SystemInfo["StandbyLED"]
SystemInfo["PowerOffDisplay"] = HardwareInfo().get_device_model() not in "formuler1" and fileCheck("/proc/stb/power/vfd") or fileCheck("/proc/stb/lcd/vfd")
SystemInfo["WakeOnLAN"] = not HardwareInfo().get_device_model().startswith("et8000") and fileCheck("/proc/stb/power/wol") or fileCheck("/proc/stb/fp/wol")
SystemInfo["HasExternalPIP"] = not (HardwareInfo().get_device_model().startswith("et9") or HardwareInfo().get_device_model() in ('e4hd',)) and fileCheck("/proc/stb/vmpeg/1/external")
SystemInfo["VideoDestinationConfigurable"] = fileExists("/proc/stb/vmpeg/0/dst_left")
SystemInfo["hasPIPVisibleProc"] = fileCheck("/proc/stb/vmpeg/1/visible")
SystemInfo["MaxPIPSize"] = HardwareInfo().get_device_model() in ('hd51', 'h7', 'vs1500', 'e4hd') and (360, 288) or (540, 432)
SystemInfo["VFD_scroll_repeats"] = not HardwareInfo().get_device_model().startswith("et8500") and fileCheck("/proc/stb/lcd/scroll_repeats")
SystemInfo["VFD_scroll_delay"] = not HardwareInfo().get_device_model().startswith("et8500") and fileCheck("/proc/stb/lcd/scroll_delay")
SystemInfo["VFD_initial_scroll_delay"] = not HardwareInfo().get_device_model().startswith("et8500") and fileCheck("/proc/stb/lcd/initial_scroll_delay")
SystemInfo["VFD_final_scroll_delay"] = not HardwareInfo().get_device_model().startswith("et8500") and fileCheck("/proc/stb/lcd/final_scroll_delay")
SystemInfo["LcdLiveTV"] = fileCheck("/proc/stb/fb/sd_detach") or fileCheck("/proc/stb/lcd/live_enable")
SystemInfo["LcdLiveTVMode"] = fileCheck("/proc/stb/lcd/mode")
SystemInfo["LcdLiveDecoder"] = fileCheck("/proc/stb/lcd/live_decoder")
SystemInfo["FastChannelChange"] = False
SystemInfo["3DMode"] = fileCheck("/proc/stb/fb/3dmode") or fileCheck("/proc/stb/fb/primary/3d")
SystemInfo["3DZNorm"] = fileCheck("/proc/stb/fb/znorm") or fileCheck("/proc/stb/fb/primary/zoffset")
SystemInfo["Blindscan_t2_available"] = fileCheck("/proc/stb/info/vumodel")
SystemInfo["RcTypeChangable"] = not(HardwareInfo().get_device_model().startswith('et8500') or HardwareInfo().get_device_model().startswith('et7')) and pathExists('/proc/stb/ir/rc/type')
SystemInfo["HasFullHDSkinSupport"] = HardwareInfo().get_device_model() not in ("et4000", "et5000", "sh1", "hd500c", "hd1100", "xp1000", "lc")
SystemInfo["HasBypassEdidChecking"] = fileCheck("/proc/stb/hdmi/bypass_edid_checking")
SystemInfo["HasColorspace"] = fileCheck("/proc/stb/video/hdmi_colorspace")
SystemInfo["HasColorspaceSimple"] = SystemInfo["HasColorspace"] and HardwareInfo().get_device_model() in "vusolo4k"
SystemInfo["HasMultichannelPCM"] = fileCheck("/proc/stb/audio/multichannel_pcm")
SystemInfo["HasMMC"] = fileExists("/proc/cmdline") and "root=/dev/mmcblk" in open("/proc/cmdline", "r").read()
SystemInfo["HasTranscoding"] = pathExists("/proc/stb/encoder/0") or fileCheck("/dev/bcm_enc0")
SystemInfo["HasH265Encoder"] = fileHas("/proc/stb/encoder/0/vcodec_choices", "h265")
SystemInfo["CanNotDoSimultaneousTranscodeAndPIP"] = HardwareInfo().get_device_model() in "vusolo4k"
SystemInfo["HasColordepth"] = fileCheck("/proc/stb/video/hdmi_colordepth")
SystemInfo["HasFrontDisplayPicon"] = HardwareInfo().get_device_model() in ("vusolo4k", "et8500")
SystemInfo["Has24hz"] = fileCheck("/proc/stb/video/videomode_24hz")
SystemInfo["Has2160p"] = fileHas("/proc/stb/video/videomode_preferred", "2160p50")
SystemInfo["HasHDMIpreemphasis"] = fileCheck("/proc/stb/hdmi/preemphasis")
SystemInfo["HasColorimetry"] = fileCheck("/proc/stb/video/hdmi_colorimetry")
SystemInfo["HasHdrType"] = fileCheck("/proc/stb/video/hdmi_hdrtype")
SystemInfo["HasHDMI-CEC"] = HardwareInfo().has_hdmi() and fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/HdmiCEC/plugin.pyo") and (fileExists("/dev/cec0") or fileExists("/dev/hdmi_cec") or fileExists("/dev/misc/hdmi_cec0"))
SystemInfo["HasYPbPr"] = HardwareInfo().get_device_model() in ("dm8000", "et5000", "et6000", "et6500", "et9000", "et9200", "et9500", "et10000", "formuler1", "mbtwinplus", "spycat", "vusolo", "vuduo", "vuduo2", "vuultimo")
SystemInfo["HasScart"] = HardwareInfo().get_device_model() in ("dm8000", "et4000", "et6500", "et8000", "et9000", "et9200", "et9500", "et10000", "formuler1", "hd1100", "hd1200", "hd1265", "hd2400", "vusolo", "vusolo2", "vuduo", "vuduo2", "vuultimo", "vuuno", "xp1000")
SystemInfo["HasSVideo"] = HardwareInfo().get_device_model() in ("dm8000")
SystemInfo["HasComposite"] = HardwareInfo().get_device_model() not in ("i55", "gbquad4k", "gbue4k", "hd1500", "osnino", "osninoplus", "purehd", "purehdse", "revo4k", "vusolo4k", "vuzero4k")
SystemInfo["HasAutoVolume"] = fileExists("/proc/stb/audio/avl_choices") and fileCheck("/proc/stb/audio/avl")
SystemInfo["HasAutoVolumeLevel"] = fileExists("/proc/stb/audio/autovolumelevel_choices") and fileCheck("/proc/stb/audio/autovolumelevel")
SystemInfo["Has3DSurround"] = fileExists("/proc/stb/audio/3d_surround_choices") and fileCheck("/proc/stb/audio/3d_surround")
SystemInfo["Has3DSpeaker"] = fileExists("/proc/stb/audio/3d_surround_speaker_position_choices") and fileCheck("/proc/stb/audio/3d_surround_speaker_position")
SystemInfo["Has3DSurroundSpeaker"] = fileExists("/proc/stb/audio/3dsurround_choices") and fileCheck("/proc/stb/audio/3dsurround")
SystemInfo["Has3DSurroundSoftLimiter"] = fileExists("/proc/stb/audio/3dsurround_softlimiter_choices") and fileCheck("/proc/stb/audio/3dsurround_softlimiter")
SystemInfo["hasXcoreVFD"] = HardwareInfo().get_device_model() in ('osmega','spycat4k','spycat4kmini','spycat4kcombo') and fileCheck("/sys/module/brcmstb_%s/parameters/pt6302_cgram" % HardwareInfo().get_device_model())
SystemInfo["HasOfflineDecoding"] = HardwareInfo().get_device_model() not in ('osmini', 'osminiplus', 'et7000mini', 'et11000', 'mbmicro', 'mbtwinplus', 'mbmicrov2', 'et7000', 'et8500')
SystemInfo["HasRootSubdir"] = fileHas("/proc/cmdline", "rootsubdir=")
SystemInfo["canMultiBoot"] = SystemInfo["HasRootSubdir"] and (1, 4, "mmcblk0", False) or fileHas("/proc/cmdline", "_4.boxmode=") and (1, 4, "mmcblk0", False) or HardwareInfo().get_device_model() in ('gbue4k', 'gbquad4k') and (3, 3, "mmcblk0", True) or HardwareInfo().get_device_model() in ('e4hd') and (1, 4, "mmcblk0", False) or HardwareInfo().get_device_model() in ('osmio4k', 'osmio4kplus') and (1, 4, "mmcblk1", True)
SystemInfo["canMode12"] = fileHas("/proc/cmdline", "_4.boxmode=1 ") and '192M' or fileHas("/proc/cmdline", "_4.boxmode=12") and '192M'
SystemInfo["canFlashWithOfgwrite"] = not(HardwareInfo().get_device_model().startswith("dm"))
SystemInfo["HDRSupport"] = fileExists("/proc/stb/hdmi/hlg_support_choices") and fileCheck("/proc/stb/hdmi/hlg_support")
SystemInfo["CanDownmixAC3"] = fileHas("/proc/stb/audio/ac3_choices", "downmix")
SystemInfo["CanDownmixDTS"] = fileHas("/proc/stb/audio/dts_choices", "downmix")
SystemInfo["CanDownmixAAC"] = fileHas("/proc/stb/audio/aac_choices", "downmix")
SystemInfo["HDMIAudioSource"] = fileCheck("/proc/stb/hdmi/audio_source")
