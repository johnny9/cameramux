from zope.interface import implements

from twisted.internet import reactor
from twisted.web import proxy, server, resource, static
from twisted.python import log
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import FilePasswordDB
from twisted.web.guard import HTTPAuthSessionWrapper, DigestCredentialFactory

class UserRealm(object):
	implements(IRealm)

	def requestAvatar(self, avatarId, mind, *interfaces):
		print interfaces
		return (resource.IResource, CameraMux(), lambda: None)

class CameraMux(resource.Resource):
	def getChild(self, path, request):
		print 'hello world'
		print path
		if path == 'camera1': 
			return proxy.ReverseProxyResource('192.168.0.127', 80, 'video.cgi')
		if path == 'camera2':
			return proxy.ReverseProxyResource('192.168.0.136', 80, 'video.cgi')
		if path == 'camera3':
			return proxy.ReverseProxyResource('192.168.0.145', 80, 'video.cgi')
		return static.File("video.html")

portal = Portal(UserRealm(), [FilePasswordDB('httpd.password')])

credentialFactory = DigestCredentialFactory("md5", "localhost:8080")
site = server.Site(HTTPAuthSessionWrapper(portal, [credentialFactory]))
reactor.listenTCP(8080, site)
reactor.run()