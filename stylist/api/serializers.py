# --------------------------------------------
# Copyright 2020, Grant Viklund
# @Author: Grant Viklund
# @Date:   2020-10-02 17:04:26
# --------------------------------------------

from rest_framework import serializers

from stylist.models import Style

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ("name", "enabled")
