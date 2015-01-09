app.controller("mainController", function($scope, $resource, ConfigService) {
	$scope.init = function() {
		$scope.ajax.readAllConfig(function(response){
			if(response){
				$scope.configurations = response;
			} else{
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
			}
		});
    };

    var isConfigSelected = false;
	$scope.saveRow = function(){	
		var selectedRow;
		if(isConfigSelected){
			selectedRow = $(".configList>tr").index($(".configList>tr.success"));
			if(selectedRow>=0){
				$scope.configurations[selectedRow].path = $scope.path;
				$scope.configurations[selectedRow].method = $scope.method;
				$scope.configurations[selectedRow].response = $scope.response;

				$(".configList>tr.success").removeClass("success");
				isConfigSelected = false;
			}

		} else{
			$scope.configurations.push({ 'path':$scope.path, 'method': $scope.method, 'response':$scope.response });
			selectedRow = $scope.configurations.length-1;
		}
		$scope.ajax.updateConfig(function(response){
			alert("Update config "+ ((response)?"Succed": "Failed"));
		}, $scope.configurations[selectedRow]);

		$scope.path='';
		$scope.method='';
		$scope.response='';
	};	
	
	$scope.removeRow = function(path){				
		var index = _findRowIndex(path);
		$scope.configurations.splice( index, 1 );		

		$scope.ajax.deleteConfig(function(response){
			alert("Delete config "+ ((response)?"Succed": "Failed"));
		}, path);
	};

	$scope.editRow = function(path){
		var index = _findRowIndex(path);
		
		$(".configList>tr.success").removeClass("success");
		if(index>=0){
			$(".configList>tr").eq(index).addClass("success");

			$scope.path = $scope.configurations[index].path;
			$scope.method = $scope.configurations[index].method;
			$scope.response = $scope.configurations[index].response;
			isConfigSelected = true;
		}
	};

	function _findRowIndex(path){
		var index = -1;		
		var comArr = eval( $scope.configurations );
		for( var i = 0; i < comArr.length; i++ ) {
			if( comArr[i].path === path ) {
				index = i;
				break;
			}
		}
		return index;
	}


	/*
	*	REST Executor section
	*/
	$scope.ajax = {
		readAllConfig : function(callback){
			ConfigService.retrieveConfig(function(){
				callback.call(null, []);
			},function(){
				callback.call(null);
			});
		}, 
		updateConfig : function(callback, cofigInfo){
			ConfigService.storeConfig(cofigInfo, function(){
				callback.call(null, true);
			},function(){
				callback.call(null, false);
			});
		}, 
		deleteConfig : function(callback, cofigPath){
			ConfigService.eraseConfig(cofigPath, function(){
				callback.call(null, true);
			},function(){
				callback.call(null, false);
			});
		}
	}
	
	
});

