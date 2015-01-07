var app = angular.module('ApiboxUI',['ngResource'])
	.factory("ConfigService", function ($resource)
	  {
	    // Construct a resource object that can
	    // interact with the RESTful API of the server.
	    var resource = $resource("config/:operation");

	    // Custom function to retrieve a config List
	    resource.retrieveConfig = function (successCallback, errorCallback) {
	      return this.get(
	        {
	          operation: "retrieve"
	        }, successCallback, errorCallback);
	    };

	    // Custom function to save a config object
	    resource.storeConfig = function (config, successCallback, errorCallback) {
	      return this.save(
	        {
	          operation: "store",
	          path: config.path,
	          method: config.method,
	          response: config.response,
	        }, successCallback, errorCallback
	      );
	    };

	    // Custom function to delete a config object by path
	    resource.eraseConfig = function (configPath, successCallback, errorCallback) {
	      return this.delete(
	        {
	          operation: "erase",
	          path: configPath
	        }, successCallback, errorCallback);
	    };

	    return resource;
	  });
