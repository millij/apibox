var app = angular.module('ApiboxUI',['ngRoute', 'ngResource'])
	.factory("ConfigService", function ($resource)
	  {
	    // Construct a resource object that can
	    // interact with the RESTful API of the server.
	    var resource = $resource("app/:appname");

	    // Custom function to retrieve a config List
	    resource.retrieveConfig = function (appName, successCallback, errorCallback) {
	      return this.get(
	        {
	          appname: appName
	        }, successCallback, errorCallback);
	    };

	    // Custom function to save a config object
	    resource.storeConfig = function (appName, config, successCallback, errorCallback) {
	      return this.save(
	        {
	          appname: appName,
	          path: config.path,
	          method: config.method,
	          response: config.response,
	        }, successCallback, errorCallback
	      );
	    };

	    // Custom function to delete a config object by path
	    resource.eraseConfig = function (appName, configPath, successCallback, errorCallback) {
	      return this.delete(
	        {
	          appname: appName,
	          path: configPath
	        }, successCallback, errorCallback);
	    };

	    return resource;
	  });
