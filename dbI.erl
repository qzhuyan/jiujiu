-module(dbI).
-export([hello/0]).
-vsn(1.0).
-compile(export_all).

hello() ->
    io:format("DJ max!").
