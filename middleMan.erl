%%%-------------------------------------------------------------------
%%% @author  <Administrator@EZPC>
%%% @copyright (C) 2011, 
%%% @doc
%%%
%%% @end
%%% Created :  6 Mar 2011 by  <Administrator@EZPC>
%%%-------------------------------------------------------------------
-module(middleMan).

-behaviour(gen_server).

%% Compile and include
-compile(export_all).
-include("dbrecords.hrl").

%% API
-export([start_link/0]).

%% gen_server callbacks
-export([init/1, handle_call/3, handle_cast/2, handle_info/2,
	 terminate/2, code_change/3]).

-define(SERVER, ?MODULE). 

-record(state, {}).

%%%===================================================================
%%% API
%%%===================================================================

%%--------------------------------------------------------------------
%% @doc
%% Starts the server
%%
%% @spec start_link() -> {ok, Pid} | ignore | {error, Error}
%% @end
%%--------------------------------------------------------------------
start_link() ->
    start_link(5,5060).

start_link(Workers,Port) ->
    gen_server:start_link({local, ?SERVER}, ?MODULE, [5,5060], []).

%%%===================================================================
%%% gen_server callbacks
%%%===================================================================

%%--------------------------------------------------------------------
%% @private
%% @doc
%% Initializes the server
%%
%% @spec init(Args) -> {ok, State} |
%%                     {ok, State, Timeout} |
%%                     ignore |
%%                     {stop, Reason}
%% @end
%%--------------------------------------------------------------------
init([Num,LPort]) ->
    case gen_tcp:listen(LPort,[binary,{active, false},{packet_size,200}]) of
        {ok, ListenSock} ->
            start_servers(Num,ListenSock),
            {ok, Port} = inet:port(ListenSock),
            Port;
        {error,Reason} ->
            {error,Reason}
    end,

    {ok, #state{}}.

%%--------------------------------------------------------------------
%% @private
%% @doc
%% Handling call messages
%%
%% @spec handle_call(Request, From, State) ->
%%                                   {reply, Reply, State} |
%%                                   {reply, Reply, State, Timeout} |
%%                                   {noreply, State} |
%%                                   {noreply, State, Timeout} |
%%                                   {stop, Reason, Reply, State} |
%%                                   {stop, Reason, State}
%% @end
%%--------------------------------------------------------------------
handle_call(_Request, _From, State) ->
    Reply = ok,
    {reply, Reply, State}.

%%--------------------------------------------------------------------
%% @private
%% @doc
%% Handling cast messages
%%
%% @spec handle_cast(Msg, State) -> {noreply, State} |
%%                                  {noreply, State, Timeout} |
%%                                  {stop, Reason, State}
%% @end
%%--------------------------------------------------------------------
handle_cast(_Msg, State) ->
    {noreply, State}.

%%--------------------------------------------------------------------
%% @private
%% @doc
%% Handling all non call/cast messages
%%
%% @spec handle_info(Info, State) -> {noreply, State} |
%%                                   {noreply, State, Timeout} |
%%                                   {stop, Reason, State}
%% @end
%%--------------------------------------------------------------------
handle_info(_Info, State) ->
    {noreply, State}.

%%--------------------------------------------------------------------
%% @private
%% @doc
%% This function is called by a gen_server when it is about to
%% terminate. It should be the opposite of Module:init/1 and do any
%% necessary cleaning up. When it returns, the gen_server terminates
%% with Reason. The return value is ignored.
%%
%% @spec terminate(Reason, State) -> void()
%% @end
%%--------------------------------------------------------------------
terminate(_Reason, _State) ->
    ok.

%%--------------------------------------------------------------------
%% @private
%% @doc
%% Convert process state when code is changed
%%
%% @spec code_change(OldVsn, State, Extra) -> {ok, NewState}
%% @end
%%--------------------------------------------------------------------
code_change(_OldVsn, State, _Extra) ->
    {ok, State}.

%%%===================================================================
%%% Internal functions
%%%===================================================================


%%%
%%% Version History
%%%


%%%
%%% Include Files 
%%%


%%%
%%% Functions
%%%
start() ->
    start(2,5060).

start(Num,LPort) ->
    case gen_tcp:listen(LPort,[binary,{active, false},{packet_size,200}]) of
        {ok, ListenSock} ->
            start_servers(Num,ListenSock),
            {ok, Port} = inet:port(ListenSock),
            Port;
        {error,Reason} ->
            {error,Reason}
    end.

start_servers(0,_) ->
    ok;

start_servers(Num,LS) ->
    spawn(?MODULE,server,[LS]),
    start_servers(Num-1,LS).

server(LS) ->
    case gen_tcp:accept(LS) of
        {ok,S} ->
            loop(S),
            ?MODULE:server(LS);
        Other ->
            io:format("accept returned ~w - goodbye!~n",[Other]),
            ok
    end.

loop(S) ->
    inet:setopts(S,[{active,once}]),
    receive
        {tcp,S,Data} ->
            Answer = ?MODULE:process(Data), 
	    io:format("Ans is ~p",[Answer]),
            gen_tcp:send(S,erlang:term_to_binary(Answer)),
            loop(S);
        {tcp_closed,S} ->
            io:format("Socket ~w closed [~w]~n",[S,self()]),
            ok
    end.

%% Old_test_process(Data) ->
%%     OUT = erlang:binary_to_term(Data),
%%     io:format("We got ~p~n",[OUT]),
%%     io:format("ÄãºÃ"),
%%     io:format("We got ~p~n",[unicode:characters_to_list(OUT,unicode)]),
%%     erlang:term_to_binary(OUT).

process(In) ->
    case erlang:binary_to_term(In) of
	{req,[rec,Transcation],Record} ->
	    io:format("Got req:rec ,~p ~p~n",[Transcation,Record]),
	    Reply = ?MODULE:do_record(Record),
	    {rep,[rec,Transcation],Reply};
	{req,[get,Transcation],Record} ->
	    io:format("Got req:rec ,~p ~p~n",[Transcation,Record]),
	    Reply = ?MODULE:do_record(Record),
	    {rep,[rec,Transcation],Reply};

	Unkonwn ->
	    io:format("unknow cmd!"),
	    io:format("Got In: ~p~n",[Unkonwn]),
	    {sta,unknow}
    end.

   
do_record(Record) ->
    R = #workRecord{
      index = get_value(Record,datatag),
      time = get_value(Record,time),
      emp_no = get_value(Record,uid),
      product = get_value(Record,product), 
      machine = get_value(Record,machine), 
      shift = get_value(Record,shift),
      parms = get_value(Record,parms)
     },
    jiujiuDB:add_record(R).



get_value(TupleList,Key) ->
    {value,{Key,V},_}= lists:keytake(Key,1,TupleList),
    V.
    
    


       
    
