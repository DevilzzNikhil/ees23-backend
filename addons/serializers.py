from .models import Query, validate_phone_number
from rest_framework import serializers


class QuerySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    contact = serializers.CharField(required=True, validators=[validate_phone_number])
    query = serializers.CharField(required=True)

    class Meta:
        model = Query
        fields = "__all__"

    def create(self, validated_data):
        query = Query.objects.create(
            email=validated_data["email"],
        )
        query.name = validated_data["name"]
        query.contact = validated_data["contact"]
        query.query = validated_data["query"]
        query.save()
        return query
