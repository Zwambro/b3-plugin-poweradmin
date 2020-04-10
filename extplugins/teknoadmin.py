#
# PowerAdmin Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# Copyright (C) 2005 www.xlr8or.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
# Changelog:
# 1.0.0 - 1.0.1 : Patched sclient.id to sclient.cid
# 1.0.1 - 1.1.0 : Added serverside CoD2 mod and new functionality.
# 1.3.1 : New command !pamono to remove colorcodes from playernames.
# 1.3.2 : New command !panades to grant nades to a player.
# 1.3.3 : Send rcon result to client on !paexec and !pamaprestart
# 1.3.4 : Typo fixed
# 30-09-2010 - v1.3.5 : Minor updates
#

__version__ = '1.3.5'
__author__  = 'xlr8or'

import b3, re
import b3.events

#--------------------------------------------------------------------------------------------------
class teknoadminPlugin(b3.plugin.Plugin):
    _adminPlugin = None

    def startup(self):
        """\
        Initialize plugin settings
        """

        # get the admin plugin so we can register commands
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            # something is wrong, can't start without admin plugin
            self.error('Could not find admin plugin')
            return False
        
        # register our commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

        self.debug('Started')


    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None


    def onEvent(self, event):
        """\
        Handle intercepted events
        """


#--Commands implementation ------------------------------------------------------------------------

    def cmd_saybig(self, data, client, cmd=None):
        """\
        <message> - Print a Bold message on the center of all screens.
        (You can safely use the command without the 'pa' at the beginning)
        """
        if not data:
            client.message('^7Invalid or missing data, try !help saybig')
            return False
        else:
            # are we still here? Let's write it to console
            self.console.setCvar( 'b3_saybold','%s' % data )

        return True

    def cmd_nasty(self, data, client, cmd=None):
        """\
        <player> [<reason>] - Will make the game unplayable for the client. Be Carefull! Very Nasty!
        (You can safely the command without the 'pa' at the beginning)
        """
        # this will split the player name and the message
        input = self._adminPlugin.parseUserCmd(data)
        if input:
            # input[0] is the player id
            sclient = self._adminPlugin.findClientPrompt(input[0], client)
            if not sclient:
                # a player matchin the name was not found, a list of closest matches will be displayed
                # we can exit here and the user will retry with a more specific player
                return False
        else:
            client.message('^7Invalid data, try !help nasty')
            return False

        if len(input) > 1:
            sclient.message('^3Admin Retaliation: ^7%s' % (input[1]))

        # are we still here? Let's execute the retaliation
        self.console.setCvar( 'b3_r2cid','%s' % sclient.cid )

        return True


#--Original Code below by Ravir / Bulletworm ------------------------------------------------------

    def cmd_afk(self, data, client, cmd=None):
        if not data:
            client.message('^7Invalid data, try !help afk')
            return False
        else:
            self.console.setCvar( 'g_switchspec','spectator' )
            client.message('^7You are spectating now')
            return True

    #def cmd_pakillplayer(self, data, client, cmd=None):
        #"""\
        #<player> - Kill a player on the spot
        #(You can safely use the command without the 'pa' at the beginning)
        #"""
        # this will split the player name and the message
        #input = self._adminPlugin.parseUserCmd(data)
        #if input:
            ## input[0] is the player id
            #sclient = self._adminPlugin.findClientPrompt(input[0], client)
            #if not sclient:
                ## a player matchin the name was not found, a list of closest matches will be displayed
                ## we can exit here and the user will retry with a more specific player
                #return False
        #else:
            #client.message('^7Invalid data, try !help switch')
            #return False

        #if len(input) > 1:
            #sclient.message('^3You are being killed: ^7%s' % (input[1]))

        ## are we still here? Let's execute the kill
        #self.console.setCvar( 'g_killplayer','%s' % sclient.cid )

        #return True

#if __name__ == '__main__':
    #print '\nThis is version '+__version__+' by '+__author__+' for BigBrotherBot.\n'
