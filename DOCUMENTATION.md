# Options

List of supported action types.

## path

Required parameter that indicates the location and name of the databases. Can be a list.

## state

Required parameter to specify the type of action to be performed on the databases.

* present: Action for creating databases files. Returns a list of created databases.
* absent: Action for remove databases files. Returns a list of removed databases.
* request: Action for execute sqlite requests on  databases files. Also create the database file. Returns results of requests per database.
* dump: Action for dumping databases files in specified directories. Returns locations of dumps per database.

## request

Optional parameter containing the query(s) to execute on the databases. Can be a list.
	
## dumpDir

Optional parameter that indicates the location and name of the dumping directories. Can be a list.



