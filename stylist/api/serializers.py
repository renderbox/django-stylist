# --------------------------------------------
# Copyright 2020, Grant Viklund
# @Author: Grant Viklund
# @Date:   2020-10-02 17:04:26
# --------------------------------------------

from rest_framework import serializers

from stylist.models import Style, Font

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ("name", "enabled")

class FontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Font
        fields = ("pk", "family", "weights", "href")
