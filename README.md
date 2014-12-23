Introduction:
======
ApiBox is a  minimal feature tool to decouple the backend and frontend teams working on service oriented applications(SOA) by minimizing the dependencies between them. The purpose of this ApiBox is to generate mock RESTful APIs from the developer provided static data with minimal effort. This helps the team to continue developing without having to wait till the backend team provides the needed API endpoint without making any changes in the signature of the respective APIs.
<h2>
How does it work:
</h2>
<br>
1) Takes the user specified JSON and Validates with the required format of JSON
<br>
2) If user JSON satisfies with the required JSON then it extracts the endpoints mention in the json and mock them according to response provided by the user in its respective endpoint.
<h2>
How to use it:
</h2>
<br>
1) Clone ApiBox
<br>
2) Create your JSON referring to the required JSON(reference.json) and insert in box folder.
<br>
<h4>
3) And run these command
</h4>
<code>
 <br>
 make install 
 <br>
 python final.py runserver -c <conf_filename>  -t <host  (0.0.0.0)> -p <port number (9823)>

</code>
<br>
-c <filename> is to configure user json
<br>
-t <host number> is to configure user specified host
<br>
-p <port number> is to configure user specified port
 <h5>
Note:
</h5>
<br>
1) while running the apibox should specify the json file and there is no default option 
<br>
2) By default host is users local host and port number is 5000

