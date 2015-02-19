# Introduction
ApiBox is a  minimal feature tool to decouple the backend and frontend teams working on service oriented applications(SOA) by minimizing the dependencies between them. The purpose of this ApiBox is to generate mock RESTful APIs from the developer provided static data with minimal effort. This helps the team to continue developing without having to wait till the backend team provides the needed API endpoint without making any changes in the signature of the respective APIs.

#### Version
0.1

## Dependencies
### System
- python-2.7.x
- python-virtualenv

### Software
- Flask
- refer to requirements.txt

## How does it work:
- Takes the user specified JSON and Validates with the required format of JSON
- If user JSON satisfies with the required JSON then it extracts the endpoints mention in the json and mock them according to response provided by the user in its respective endpoint.

## How to use it:
- Clone ApiBox
- Create your API configuration JSON(A sample for reference is located in examples folder).

And run the below commands

```sh
$ make install
$ . envi/bin/activate
$ python box/apibox.py -f <conf_filepath>  -t <host> -p <port> 
```
Options description:
* -f : api config json filepath
* -t : host IP address (default: 127.0.0.1 / localhost)
* -p : port number (default: 5000)

### Note
- While running the apibox should specify the json file and there is no default option 
- By default host is users local host and port number is 5000


