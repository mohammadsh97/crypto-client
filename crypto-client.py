import json
import requests
import sys


def main(argv):
    if len(argv) != 3 and len(argv) != 8:
        print("python <FILE-NAME> -server-url <Server-url> -generate")
        print("OR")
        print("python <FILE-NAME> -server-url <Server-url> -operation <OPERATION> "
              "-input-file <PATH> -output-file <PATH>")
    else:
        # Generate Key
        if argv[2].__eq__("-generate"):
            response = requests.post(argv[1] + '/api/generate/')
            if response.status_code != 200:
                # This means something went wrong.
                raise Exception('Post /api/ {}'.format(response.status_code))
            json_data = response.json()

        else:
            # read input.txt file
            read = open(argv[5], "r")
            data = json.load(read)

            # Encrypt data
            if argv[3].__eq__("encrypt"):
                response = requests.post(argv[1] + '/api/encrypt',
                                         json={'keyId': data['keyId'], 'data': data['data']})
                if response.status_code != 200:
                    # This means something went wrong.
                    raise Exception('Post /api/encrypt/ {}'.format(response.status_code))

            # Decrypt data
            elif argv[3].__eq__("decrypt"):
                response = requests.post(argv[1] + '/api/decrypt',
                                         json={'keyId': data['keyId'], 'encryptedData': data['encryptedData']})

                if response.status_code != 200:
                    # This means something went wrong.
                    raise Exception('Post /api/decrypt/ {}'.format(response.status_code))

            # Sign data
            elif argv[3].__eq__("sign"):
                response = requests.post(argv[1] + '/api/sign',
                                         json={'keyId': data['keyId'], 'data': data['data']})

                if response.status_code != 200:
                    # This means something went wrong.
                    raise Exception('Post /api/sign/ {}'.format(response.status_code))

            # Verify data
            elif argv[3].__eq__("verify"):
                response = requests.post(argv[1] + '/api/verify',
                                         json={'keyId': data['keyId'], 'data': data['data'],
                                               'signature': data['signature']})

                if response.status_code != 200:
                    # This means something went wrong.
                    raise Exception('Post /api/verify/ {}'.format(response.status_code))
            else:
                raise Exception('Error <OPERATION> is not exist')

            json_data = response.json()

            # output.txt file
            with open(argv[7], 'a') as file:
                file.write(json.dumps(json_data, indent=2))
                file.write("\n")

            # close input.txt file
            read.close()

        print('Status code: ', response.status_code, "OK")
        json_formatted_str = json.dumps(json_data, indent=2)
        print(json_formatted_str)


if __name__ == "__main__":
    main(sys.argv[1:])
