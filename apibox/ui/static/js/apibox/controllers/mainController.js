app.controller("mainController", function($scope, $resource, ConfigService) {
	$scope.init = function() {
		
    };

	$scope.editRow = function(){
		var trgElm = event.target;
		var appName = $(trgElm).parent("tr").find("td:first-child").text();
		if(appName){
			$(trgElm).parent("tr").find("a").click();
		}
	};
	
});

app.config(["$routeProvider", function($routeProvider){
	$routeProvider.when('/app/:appName', {
		template: '<table style=\"width:100%\" class=\"container\">'+
		                '<tr class=\"row\">'+
		                    '<td style=\"vertical-align: top\" class=\"col-lg-5\">'+
		                        '<table class=\"table table-hover\">'+
		                            '<caption class=\"font-bold\">Select an Endpoint</caption>'+
		                            '<thead>'+
		                                '<tr>'+
		                                    '<th>Path</th>'+
		                                    '<th>Method</th>'+
		                                    '<th>Response</th>'+
		                                '</tr>'+
		                            '</thead>'+
		                            '<tbody class=\"configList\">'+
		                            '<tr ng-repeat=\"config in configurations\" >'+
	                                    '<td>{{config.path}}</td>'+
	                                    '<td>{{config.method}}</td>'+
	                                    '<td>{{config.response}}</td>'+
	                                '</tr>'+
		                            '</tbody>'+
		                        '</table>'+
		                    '</td>'+
		                '</tr>'+
		            '</table>',
		controller: 'ShowAppDeatilController'
      }).otherwise({template: '', controller: 'ShowAppListController'});
}]);


app.controller("ShowAppDeatilController", function($scope, $routeParams, ConfigService){
	$("#appTable").hide();
	ConfigService.retrieveConfig($routeParams.appName, function(){
		debugger;
	}, function(){
		debugger;
		$scope.configurations = [
		                    { 'path':'/widget',
		                    	'method': 'add',
		                    	'response': '<response/>'},
		                    	{ 'path':'/template',
			                    	'method': 'add',
			                    	'response': '<response/>'},
			                    	{ 'path':'/pins',
				                    	'method': 'add',
				                    	'response': '<response/>'},
				                    	{ 'path':'/blacklist',
					                    	'method': 'add',
					                    	'response': '<response/>'},				                    	
		                    ];
	})
	
});

app.controller("ShowAppListController", function($scope, $routeParams){
	$("#appTable").show();
});