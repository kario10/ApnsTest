from pushjack import APNSSandboxClient




def pushNotification(message):

    client = APNSSandboxClient(
        certificate= './skylovePushnotification.pem',
        default_error_timeout=10,
        default_expiration_offset=2592000,
        default_batch_size=100,
        default_retries=5
    )

    token = '68007173ada88f95f373fadfc5e17a6d3f32f2cae46a93e9c288566a826ff75f'
    alert = message



    try:
        res = client.send(
            token,
            alert,
            badge = 'badge count',
            sound = 'sound to play',
            content_available = True,
            title = 'Baraam class announcement',
        )

    finally:
        client.close()
        if res.errors != None:
            return res.errors
        return
