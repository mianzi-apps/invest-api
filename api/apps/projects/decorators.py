from rest_framework import status
from rest_framework.response import Response


def validated_data(fn):
    def decorator(*args, **kwargs):
        alias = args[0].request.data.get('alias', '')
        description = args[0].request.data.get('description', '')
        start_date = args[0].request.data.get('start_date', '')
        harvest_start_date = args[0].request.data.get('harvest_start_date', '')
        estimated_harvest_duration = args[0].request.data.get('estimated_harvest_duration', '')
        plants = args[0].request.data.get('plants', [])
        animals = args[0].request.data.get('animals', [])

        if not alias and not description and not start_date and not harvest_start_date and not estimated_harvest_duration:
            return Response(data={
                'message': 'alias, description, start_date, harvest_start_date, estimated_harvest_duration are required'
            }, status=status.HTTP_400_BAD_REQUEST
            )

        return fn(*args, **kwargs)

    return decorator


def validate_profile_data(fn):
    def decorator(*args, **kwargs):
        # project_id = kwargs['pk']
        project_stage = args[0].request.data.get('project_stage', '')
        stage_caption = args[0].request.data.get('stage_caption', '')
        detailed_explanation = args[0].request.data.get('detailed_explanation', '')
        images = args[0].request.data.get('images', [])

        if not project_stage and not stage_caption and not detailed_explanation and not images:
            return Response(
                data={'massage': 'project_stage, stage_caption, detailed_explanation, images are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorator


def validate_image_data(fn):
    def decorator(*args, **kwargs):
        image_url = args[0].request.data.get('image_url', '')

        if not image_url:
            return Response(
                data={'massage': 'image_url is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorator


def validate_animal_data(fn):
    def decorator(*args, **kwargs):
        animal_id = args[0].request.data.get('animal_id', '')
        no = args[0].request.data.get('no', '')
        if not animal_id and not no:
            return Response(
                data={'massage': 'animal id and no is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorator


def validate_plant_data(fn):
    def decorator(*args, **kwargs):
        animal_id = args[0].request.data.get('animal_id', '')
        no = args[0].request.data.get('no', '')
        if not animal_id and not no:
            return Response(
                data={'massage': 'animal id and no is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorator


def validate_expenses_data(fn):
    def decorator(*args, **kwargs):
        exp_type = args[0].request.data.get('exp_type', '')
        amount = args[0].request.data.get('amount', '')
        comment = args[0].request.data.get('comment', '')
        date_spent = args[0].request.data.get('date_spent', '')

        if not exp_type and not amount and not date_spent:
            return Response(
                data={'massage': 'exp_type amount and date_spent are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorator


def validate_earnings_data(fn):
    def decorator(*args, **kwargs):
        amount_earned = args[0].request.data.get('amount_earned', '')
        date_earned = args[0].request.data.get('date_earned', '')
        if not amount_earned and not date_earned:
            return Response(
                data={'massage': 'amount_earned and date_earned are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorator
