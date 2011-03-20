%%%-------------------------------------------------------------------
%%% @author  <Administrator@EZPC>
%%% @copyright (C) 2011, 
%%% @doc
%%%
%%% @end
%%% Created : 26 Feb 2011 by  <Administrator@EZPC>
%%%-------------------------------------------------------------------
-module(jiujiuDB).

-behaviour(gen_server).
-include("dbrecords.hrl").
%% API
-export([start_link/0,
	 add_record/1,
	 get_record/1,
	 init_empty_tables/0,
	 remove_all_tables/0,
	 debug_all/0]).

%% gen_server callbacks
-export([init/1,
	 handle_call/3,
	 handle_cast/2,
	 handle_info/2,
	 terminate/2,
	 code_change/3]).

-define(SERVER, ?MODULE). 

-record(state, {tableList, %% Table of this server maintance
		nodeList
	 }).

%%%===================================================================
%%% API
%%%===================================================================
add_record(Record)->
    gen_server:call(?MODULE,{add,Record}).

get_record(Key)->
    gen_server:call(?MODULE,{get,Key}).
	   
init_empty_tables()->
    gen_server:call(?MODULE,initDB).

debug_all() ->    
    dbg:tracer(),
    dbg:p(all, [c]),
    dbg:tpl(?MODULE,[{'_', [], [{return_trace}]}]).

remove_all_tables() ->
    mnesia:delete_table(colMap),
    mnesia:delete_table(workRecord).
    
    
%%--------------------------------------------------------------------
%% @doc
%% Starts the server
%%
%% @spec start_link() -> {ok, Pid} | ignore | {error, Error}
%% @end
%%--------------------------------------------------------------------
start_link() ->
    gen_server:start_link({local, ?SERVER}, ?MODULE, [], []).

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
init([]) ->
    mnesia:start(),
    mnesia:subscribe({table,colMap,simple}),
    {ok, #state{nodeList=[node()]}}.

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

%%initDB create new DB, for newly installion
handle_call(initDB, _From, State) ->
    stopped = mnesia:stop(),
    ok = mnesia:delete_schema([node()]),
    Reply = create_empty_tables(State#state.nodeList),
    {reply, Reply, State};

handle_call({match,RecordPattern}, _From, State) ->
    Reply = mnesia:transaction(fun()-> mnesia:match_object(RecordPattern) end),
    {reply,Reply,State};


handle_call({get,Key}, _From, State) when is_integer(Key)->
    {atomic,[Result]} = mnesia:transaction(fun()-> mnesia:read({workRecord,Key}) end),
    [workRecord|Values] = tuple_to_list(Result),
    Reply = lists:zip(mnesia:table_info(workRecord,attributes),Values),
    {reply,Reply,State};

%% handle_call({get,Key}, _From, State) when is_list(Key)->
%%     Reply = mnesia:transaction(fun()-> mnesia:read({workRecord,list_to_integer(Key)}) end),
%%     {reply,Reply,State};

handle_call({add,Record}, _From, State) ->
    {NewRowsToBeAdd,FormedRecord} = mapping_to_workRecord_table(Record),
    Reply = case NewRowsToBeAdd of 
		      [] ->
			  mnesia:transaction(fun()-> mnesia:write(FormedRecord) end);
		      NewRowsToBeAdd ->
			  ok = add_colMap(NewRowsToBeAdd),
			  mnesia:transaction(fun()-> mnesia:write(FormedRecord) end)
	    end,
    {reply,Reply,State};


handle_call({update_attrlist,Table,NewAttrList}, _From, State) ->
    TransFun = fun(X) ->
		       NewAttrs = NewAttrList -- X,
		       list_to_tuple([tuple_to_list(X)|NewAttrs])
	       end,
    Reply = mnesia:transform_table(Table,TransFun,NewAttrList), 
    {reply, Reply, State};

handle_call({mfa,?MFAMagicCode,[M,F,A]}, _From, State) ->
    Reply = apply(M,F,A),
    {reply, Reply, State};
    
handle_call(_Request, _From, State) ->
    Reply = unknown_request,
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
handle_cast({add,Record}, State) when is_list(Record) ->
    {NewRowsToBeAdd,FormedRecord} = mapping_to_workRecord_table(Record),
    {atomic,ok} = case NewRowsToBeAdd of 
		      [] ->
			  mnesia:transaction(fun()-> mnesia:write(FormedRecord) end);
		      NewRowsToBeAdd ->
			  ok = add_colMap(NewRowsToBeAdd),
			  mnesia:transaction(fun()-> mnesia:write(FormedRecord) end)
		  end,
    {noreply, State};

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
handle_info({mnesia_table_event,{write, NewRecord, _ActivityId}}, State) when is_record(NewRecord,colMap) ->
    %% io:format("get ~n~p~n",[NewRecord]),
    %% {atomic, NewAttrList} = 
    %% 	mnesia:transaction(
    %% 	  fun() ->
    %% 		  AttrName = case NewRecord#colMap.attrName of
    %% 				 Attr when is_list(Attr) ->
    %% 				     list_to_atom(Attr);
    %% 				 Attr when is_integer(Attr) ->
    %% 				     list_to_atom(integer_to_list(Attr));
    %% 				 AtomAttr when is_atom(AtomAttr) ->
    %% 				     AtomAttr
    %% 			     end,
    %% 		  %{atomic,OldAttrKeys} = mnesia:all_keys(colMap),
    %% 		  OldAttrs = mnesia:table_info(workRecord,attributes),
    %% 		  OldAttrs ++ [AttrName]
    %% 	  end
    %% 	 ),
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
create_empty_tables(NodeList) ->
    ok = mnesia:create_schema([node()]),
    ok = mnesia:start(),
    {_,ok} = mnesia:create_table(colMap,[{attributes,record_info(fields, colMap)},{record_name, colMap},{disc_copies,[node()]}]),
    {_,ok} = mnesia:create_table(workRecord,[{attributes,[timetag,time]},{disc_copies,[node()]}]).

    
mapping_to_workRecord_table(TupleList) ->
    AttrList = mnesia:table_info(workRecord,attributes),
    DefalutValueList = lists:duplicate(length(AttrList),""),
    WorkRecordRecord = lists:zip(AttrList,DefalutValueList),
    {SortedNewAttrList,SortedValueList} = lists:unzip(map_to_attr_list(WorkRecordRecord,TupleList)),
    NewAttrs = SortedNewAttrList -- AttrList,
    {NewAttrs,list_to_tuple([workRecord] ++ SortedValueList)}.

map_to_attr_list(AttrList,[]) ->
    AttrList;
map_to_attr_list(AttrList,[{K,V}|T]) ->
    map_to_attr_list(lists:keystore(K,1,AttrList,{K,V}),T).

add_colMap([]) ->
    ok;
add_colMap([X|T]) ->
    {atomic, NewAttrList} = 
    mnesia:transaction(fun() -> 
			       AttrName = case X of
					      Attr when is_list(Attr) ->
						  list_to_atom(Attr);
					      Attr when is_integer(Attr) ->
						  list_to_atom(integer_to_list(Attr));
					      AtomAttr when is_atom(AtomAttr) ->
						  AtomAttr
					  end,
			       mnesia:write({colMap,AttrName,added}),
			       OldAttrs = mnesia:table_info(workRecord,attributes),
			       OldAttrs ++ [AttrName]
			       
		
		       end),
    {atomic,ok} = mnesia:transform_table(workRecord,ignore,NewAttrList), 
    add_colMap(T).
    
    
    
    
    
    
	
    
