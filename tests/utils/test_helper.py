"""
Unit tests for obdii.utils.helper module.
"""
from obdii.utils.helper import override_class_attributes


class TestOverrideClassAttributes:
    """Test suite for override_class_attributes function."""

    def test_override_existing_attributes(self):
        """Test overriding existing class attributes."""
        class TestClass:
            attr1 = "default1"
            attr2 = "default2"
        
        obj = TestClass()
        override_class_attributes(obj, {"attr1": "value1"}, attr1="new1", attr2="new2")
        
        assert obj.attr1 == "new1"
        assert obj.attr2 == "default2"

    def test_override_with_pop(self):
        """Test override with pop=True consumes kwargs during override."""
        class TestClass:
            attr1 = "default1"
            attr2 = "default2"
        
        obj = TestClass()
        kwargs = {"attr1": "new1", "attr3": "extra"}
        
        # When pop=True, kwargs get consumed (popped) from the dict passed to the function
        # This is useful in constructors to process known args and leave unknown ones
        override_class_attributes(obj, {"attr1": "value1", "attr2": "value2"}, pop=True, **kwargs.copy())
        
        assert obj.attr1 == "new1"
        assert obj.attr2 == "default2"

    def test_override_creates_new_attributes(self):
        """Test overriding can create new attributes."""
        class TestClass:
            pass
        
        obj = TestClass()
        override_class_attributes(obj, {"new_attr": "default"}, new_attr="value")
        
        assert obj.new_attr == "value" # type: ignore[attr-defined]

    def test_override_uses_default_when_kwarg_missing(self):
        """Test uses default value when kwarg not provided."""
        class TestClass:
            attr1 = "original"
        
        obj = TestClass()
        override_class_attributes(obj, {"attr1": "default", "attr2": "default2"})
        
        assert obj.attr1 == "default"
        assert obj.attr2 == "default2" # type: ignore[attr-defined]
