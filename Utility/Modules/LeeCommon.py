# -*- coding: UTF-8 -*-

import os
import sys
import platform

class _LeeCommon:
	'''
	这个类用来存放一些通用的函数
	此类中的任何一个方法都可以被独立使用, 无需依赖
	'''
	def verifyAgentLocation(self):
		'''
		用于验证此脚本是否处于正确的运行位置
		'''
		scriptDir = self.getScriptDirectory()
		leeClientDir = self.getLeeClientDirectory()
		verifyPassFlag = True
		
		# 检查脚本所在的目录中, 是否存在特定的平级目录
		verifyDirList = ['Bin', 'Modules', 'Patches']
		for dir in verifyDirList:
			verifyPath = (os.path.abspath(scriptDir + dir) + os.sep)
			if False == (os.path.isdir(verifyPath) and os.path.exists(verifyPath)):
				verifyPassFlag = False
		
		# 检查脚本所在的上级目录中, 是否存在特定的文件
		verifyFileList = ['cps.dll', 'aossdk.dll']
		for file in verifyFileList:
			verifyPath = (os.path.abspath(leeClientDir + file))
			if False == (os.path.isfile(verifyPath) and os.path.exists(verifyPath)):
				verifyPassFlag = False
		
		# 任何一个不通过, 都认为脚本所处的位置不正确
		return verifyPassFlag

	def removeEmptyDirectorys(self, folderpath):
		'''
		递归移除指定目录中的所有空目录
		'''
		for parent, _dirnames, _filenames in os.walk(folderpath, topdown = False):
			if not os.listdir(parent):
				os.rmdir(parent)

	def getScriptDirectory(self):
		'''
		获取当前脚本所在的上级目录位置 (末尾自动补充斜杠)
		'''
		return os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], '..')) + os.sep

	def getLeeClientDirectory(self):
		'''
		获取 LeeClient 的主目录 (末尾自动补充斜杠)
		'''
		scriptDir = self.getScriptDirectory()
		return os.path.abspath(os.path.join(scriptDir, '..')) + os.sep

	def getBeforePatchesDirectory(self):
		'''
		获取通用的 BeforePatches 目录 (末尾自动补充斜杠)
		'''
		scriptDir = self.getScriptDirectory()
		return os.path.abspath("%s/Patches/Common/BeforePatches" % scriptDir) + os.sep

	def getAfterPatchesDirectory(self):
		'''
		获取通用的 AfterPatches 目录 (末尾自动补充斜杠)
		'''
		scriptDir = self.getScriptDirectory()
		return os.path.abspath("%s/Patches/Common/AfterPatches" % scriptDir) + os.sep

	def getClientBuildDirectory(self, clientver):
		'''
		获取客户端版本的 Build 目录 (末尾自动补充斜杠)
		'''
		scriptDir = self.getScriptDirectory()
		return os.path.abspath("%s/Patches/RagexeClient/%s/Ragexe/Build" % (scriptDir, clientver)) + os.sep
	
	def getClientOriginDirectory(self, clientver):
		'''
		获取客户端版本的 Original 目录 (末尾自动补充斜杠)
		'''
		scriptDir = self.getScriptDirectory()
		return os.path.abspath("%s/Patches/RagexeClient/%s/Resource/Original" % (scriptDir, clientver)) + os.sep
	
	def getClientTranslatedDirectory(self, clientver):
		'''
		获取客户端版本的 Translated 目录 (末尾自动补充斜杠)
		'''
		scriptDir = self.getScriptDirectory()
		return os.path.abspath("%s/Patches/RagexeClient/%s/Resource/Translated" % (scriptDir, clientver)) + os.sep

	def getRagexeClientList(self, dirpath):
		'''
		根据指定的 dir 中枚举出子目录的名字
		这里的目录名称为 Ragexe 客户端版本号的日期
		
		返回: Array 保存着每个子目录名称的数组
		'''
		dirlist = []
		
		try:
			list = os.listdir(dirpath)
		except:
			print("getRagexeClientList Access Deny")
			return None
		
		for dname in list:
			if os.path.isdir(os.path.normpath(dirpath) + os.path.sep + dname):
				dirlist.append(dname)
		
		dirlist.sort()
		return dirlist

	def cleanScreen(self):
		'''
		用于清理终端的屏幕 (Win下测试过, Linux上没测试过)
		'''
		sysstr = platform.system()
		if (sysstr == 'Windows'):
			os.system('cls')
		else:
			os.system('clear')

	def pauseScreen(self):
		'''
		如果在 Win 平台下的话, 输出一个 pause 指令
		'''
		sysstr = platform.system()
		if (sysstr == 'Windows'):
			os.system('pause')

	def exitWithMessage(self, message):
		'''
		抛出一个错误消息并终止脚本的运行
		'''
		print(message + '\r\n')
		
		self.pauseScreen()
		sys.exit(0)

	def isDirectoryExists(self, dirpath):
		'''
		判断指定的目录是否存在
		'''
		return os.path.exists(dirpath) and os.path.isdir(dirpath)

	def isFileExists(self, filepath):
		'''
		判断指定的文件是否存在
		'''
		return os.path.exists(filepath) and os.path.isfile(filepath)

	def atoi(self, val):
		'''
		用于将一个字符串尝试转换成 Int 数值
		转换成功则返回 Int 数值，失败则返回布尔类型的 False
		'''
		try:
			int(val)
			return int(val)
		except ValueError:
			return False
	
	def getStringWidthLen(self, val):
		'''
		计算字符串长度, 一个中文算两个字符
		'''
		length = len(val)
		utf8_length = len(val.encode('utf-8'))
		return int((utf8_length - length)/2 + length)

	def simpleConfirm(self, lines, title, prompt, menus, evalcmd):
		'''
		简易的确认对话框
		'''
		self.cleanScreen()
		if not title is None:
			titleFmt = '= %s%-' + str(60 - self.getStringWidthLen(title)) + 's ='
			print('================================================================')
			print(titleFmt % (title, ''))
			print('================================================================')
		
		for line in lines:
			print(line)
		
		print('')
		user_select = input(prompt + ' [Y/N]: ')
		print('----------------------------------------------------------------')
		
		if user_select in ('N', 'n'):
			menus.item_End()
		elif user_select in ('Y', 'y'):
			eval(evalcmd)
		else:
			self.exitWithMessage('请填写 Y 或者 N 之后回车确认, 请不要输入其他字符')

	def simpleMenu(self, items, title, prompt, menus, withcancel = False):
		'''
		简易的选择菜单
		'''
		self.cleanScreen()
		if not title is None:
			titleFmt = '= %s%-' + str(60 - self.getStringWidthLen(title)) + 's ='
			print('================================================================')
			print(titleFmt % (title, ''))
			print('================================================================')
		
		print('')
		index = 0
		for item in items:
			print('%d - %s' % (index, item[0]))
			index = index + 1
		if withcancel:
			print('%d - %s' % (index, "取消"))
		print('')
		userSelect = input('%s (%d - %d): ' % (prompt, 0, len(items) - 1))
		print('----------------------------------------------------------------')
		
		if (False == self.atoi(userSelect) and userSelect != '0'):
			self.exitWithMessage('请填写正确的菜单编号(纯数字), 不要填写其他字符')
			
		userSelect = self.atoi(userSelect)

		if (userSelect == len(items) and withcancel):
			eval("menus.item_Main()")
			return
		
		if (userSelect >= len(items) or items[userSelect] is None):
			self.exitWithMessage('请填写正确的菜单编号(纯数字), 不要超出范围')
		elif (items[userSelect][1] is not None):
			eval(items[userSelect][1])
		
		return self.atoi(userSelect)