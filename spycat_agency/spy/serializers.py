from rest_framework import serializers
from .models import Cat, Mission, Target
from .helpers import validate_breed


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']

    def validate_breed(self, value):
        if not validate_breed(value):
            raise serializers.ValidationError("Invalid breed. Please provide a valid cat breed.")
        return value


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_complete']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'is_complete', 'targets']

    def validate(self, data):
        targets_data = data.get('targets', [])
        if not (1 <= len(targets_data) <= 3):
            raise serializers.ValidationError("A mission must have between 1 and 3 targets.")

        cat = data.get('cat')
        if cat is not None and cat.missions.filter(is_complete=False).exists():
            raise serializers.ValidationError("This cat already has an active mission.")

        return data

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)

        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission
