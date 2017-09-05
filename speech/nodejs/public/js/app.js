var app = angular.module('springml-app', []);
app.controller('MainController', function($scope, $http) {
    $scope.title = "SpringML";
    $scope.transcriptions = "";
    $scope.showSpinner = true;
    $scope.transcribe = function(data) {
        if ($scope.data.uri == data.uri) {
            $scope.transcriptions = "";
            $scope.showSpinner = false;
            $http.post('/posts', data).success(function (response){
                $scope.showSpinner = true;
                $scope.transcriptions = response.transcriptArray;
            });
        }
    };
});
