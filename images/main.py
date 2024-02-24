from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

def get_top_predicted_concept(image_path, api_key, model_id, model_version_id, user_id, app_id):
    # Read the local image file
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + api_key),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=model_id,
            version_id=model_version_id,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]

    # Get the top predicted concept
    top_concept = output.data.concepts[0]
    
    # Return the predicted concept as a tuple
    return top_concept.name, top_concept.value

# Replace with your actual values
api_key = '574e6535fb0342fb85549d47e0a6f316'
model_id = 'verssion1'
model_version_id = '7bfb29768ed548d8bf8764304aa9ba3d'
user_id = 'wn6bnlcudyt'
app_id = 'Barcode-v1-1'
image_path = '../images/media.jpg'

# Call the function to get the top predicted concept and assign it to a variable named "barcode"
barcode_name, barcode_value = get_top_predicted_concept(image_path, api_key, model_id, model_version_id, user_id, app_id)

# Print or use the "barcode" variable as needed
print("*"+barcode_name+"*")
with open('../barcode.txt', 'w') as txt_file:
    txt_file.write(barcode_name)
    
