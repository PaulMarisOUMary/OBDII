.. title:: Architecture

:description: Internal architecture of py-obdii. How Connection, Transport, Protocol, Command and Parser interact at runtime to query vehicle data via an ELM327 adapter.

.. meta::
   :keywords: py-obdii architecture, obdii library internals, elm327 python internals, obdii connection flow, python obdii protocol handler, obdii command parser python
   :robots: index, follow

Architecture
============

The diagram below shows the lifecycle of a query: from creating a
:class:`~obdii.Connection` to receiving a parsed :class:`~obdii.Response`.

.. mermaid::

   sequenceDiagram
      actor User
      participant Connection
      participant Transport
      participant Protocol
      participant Parser

      User->>Connection: Connection(...)
      Connection->>Transport: resolve & connect()
      Transport-->>Connection: OK

      rect rgba(128, 128, 128, 0.25)
         Note over Connection,Protocol: Initialization
         loop Adapter configuration
            Connection->>Transport: send AT command
            Transport-->>Connection: raw bytes
         end
         loop Vehicle protocol detection
            Connection->>Transport: try protocol
            Transport-->>Connection: raw bytes
         end
         Connection->>Protocol: get_handler(protocol id)
         Protocol-->>Connection: protocol handler
      end

      User->>Connection: conn.query(command)
      Note over Connection: Command.build() ⮞ bytes
      Connection->>Transport: write bytes
      Transport-->>Connection: raw bytes
      Note over Connection: Context(command, protocol) + raw ⮞ ResponseBase
      Connection->>Protocol: parse_response(ResponseBase)
      Protocol->>Parser: evaluate(processed bytes)
      Parser-->>Protocol: value
      Protocol-->>Connection: Response(value)
      Connection-->>User: Response