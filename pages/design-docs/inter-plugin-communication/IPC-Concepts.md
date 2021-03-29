# Concepts/Terminology

## Service Lifecycles

1) Server Startup

2) Manual Runtime Plugin Loading/Unloading

3) Requirements Based

4) Just-In-Time


## Guice

1) Insertion Points: defining DynamicMaps, DynamicSet, and DynamicItems for others to populate
(to provide implementations for)

2) APIs, defining types to be injected that others can expect a binding for

3) Defining bindings with implementattions that others can use for APIs

4) Preventing other plugins from providing implementations for APIs

5) Chaining API calls. One plugin(B) needs to call an API in another plugin(C) in order
to service the request from another plugin(A)

6) Chaining Insertion Points

7) Chaining Insertion Points to APIs

8) Chaining APIs to Insertion Points


## Classloaders

1) Mixed CL

2) Excluding CL

3) DelegatingCL

4) Sharing the minimum needed to support APIs without sharing other internal classes

5) Full sharing, acces to all classes from another plugin

6) Supporting different versions of the same library in plugins sharing classes

7) Chaining types. One plugin(B) needs to expose the type in another plugin(C) in order
to service the request from another plugin(A)


## Dependencies

1) Mandatory dependency, prevents Gerrit startup, prevents unloading, allows reloading with no downtime.

2) Runtime dependency, service cannot be provided without the dependency being loaded

3) Reloading without service interruption. A dependency can be reloaded without interrupting the
dependent service.

4) Independent aggregation, allows some services to be function without all dependencies being met

