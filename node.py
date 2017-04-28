class Node(object):
	def __init__(self, id, state, log, neighbors):
        self.id = id
        self.state = state
        self.log = log
        self.neighbors = neighbors
        self.total_nodes = 0

        self.commitIndex = 0
        self.currentTerm = 0
        self.votedFor = None

        self.lastApplied = 0

        self._lastLogIndex = 0
        self._lastLogTerm = None

        self._state.set_server(self)
        self._messageBoard.set_owner(self)

    def broadcastMessage(message):
    	for n in self.neighbors
    		message.receiver = n.id

    def sendResponse():

    def postMessage():
    	#put in self message board

    def on_message(self, message):
        """This method is called when a message is received,
        and calls one of the other corrosponding methods
        that this state reacts to.
        """
        _type = message.type

        if(message.term > self._server._currentTerm):
            self._server._currentTerm = message.term
        # Is the messages.term < ours? If so we need to tell
        #   them this so they don't get left behind.
        elif(message.term < self._server._currentTerm):
            self._send_response_message(message, yes=False)
            return self, None

        if(_type == 0): # Append Entry
            return self.onAppendEntries(message)
        elif(_type == 1): # Request vote
            a = self.onVoteRequest(message)
            return a
        elif(_type == 2): # Vote response
            return self.onVoteReceived(message)
        elif(_type == 3): # response
            return self.onResponseReceived(message)

    def onTimeout(self, message):
        """This is called when the leader timeout is reached."""

    def onVoteRequest(self, message):
        """This is called when there is a vote request."""

    def onVoteReceived(self, message):
        """This is called when this node recieves a vote."""

    def onAppendLog(self, message):
        """This is called when there is a request to
        append an entry to the log.
        """

    def onResponseReceived(self, message):
        """This is called when a response is sent back to the Leader"""

    def onClientCommand(self, message):
        """This is called when there is a client request."""

    def _nextTimeout(self):
        self.currentTime = time.time()
        return self.currentTime + random.randrange(self.timeout, 2 * self.timeout)

    def _send_response_message(self, msg, yes=True):
        response = ResponseMessage(self.id, msg.sender, msg.term, {
            "response": yes,
            "currentTerm": self.currentTerm,
        })
        self.sendResponse(response)

    def applyLog():
    	self.log[self.lastApplied]
    	self.lastApplied += 1

class State(object):
    def on_message(self, message):
        """This method is called when a message is received,
        and calls one of the other corrosponding methods
        that this state reacts to.
        """
        _type = message.type

        if(message.term > self._server._currentTerm):
            self.currentTerm = message.term
        # Is the messages.term < ours? If so we need to tell
        #   them this so they don't get left behind.
        elif(message.term < self._server._currentTerm):
            self._send_response_message(message, yes=False)
            return self, None

        if(_type == 0): # Append entries
            return self.on_append_entries(message)
        elif(_type == 1): # Request vote
            a = self.on_vote_request(message)
            return a
        elif(_type == 2): # Vote response
            return self.on_vote_received(message)
        elif(_type == 3): # Response
            return self.onResponseReceived(message)

class Leader():
	def __init__(self):
        self._nextIndexes = defaultdict(int)
        self._matchIndex = defaultdict(int)

    def onClientCommand():
    	for e in data["entries"]:
            log.append(e)
            self.commitIndex += 1

	def onResponseReceived(self, message):
		# check if append is good

	def sendLog():

    def sendHeartBeat(self):


class Candidate():
	def on_vote_request(self, message):
        

    def on_vote_received(self, message):


    def startElection(self):
    	self.currentTerm += 1
        election = RequestVoteMessage(
            self._server._name,
            None,
            self._server._currentTerm,
            {
                "lastLogIndex": self._server._lastLogIndex,
                "lastLogTerm": self._server._lastLogTerm,
            })

        self.broadcastMessage(election)
        self._last_vote = self.id

class Follower():
	def __init__(self, timeout=500):
        Voter.__init__(self)
        self._timeout = timeout
        self._timeoutTime = self._nextTimeout()

    def AppendEntries(self, message):
    	#reset timeout
    	self._timeoutTime = self._nextTimeout()

    	# Reply false if term < currentTerm (§5.1)
        if(message.term < self._server._currentTerm):
            self._send_response_message(message, yes=False)
            return self, None

        if(message.data != {}):
            log = self.log
            data = message.data
        	# Reply false if log doesn’t contain an entry at prevLogIndex whose term matches prevLogTerm
        	if(len(log) > 0 and log[data["prevLogIndex"]]["term"] != data["prevLogTerm"]):

        # If an existing entry conflicts with a new one (same index but different terms), delete the existing entry and all that follow it

        # Append any new entries not already in the log

        # If leaderCommit > commitIndex, set commitIndex = min(leaderCommit, index of last new entry)

    def 