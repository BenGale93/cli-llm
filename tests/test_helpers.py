from cli_llm import helpers


class TestGatherFileContents:
    def test_gather_with_pattern_nesting(self, func_name, temp_fs_factory):
        temp_fs = temp_fs_factory.mktemp(func_name)

        contents = ""

        temp_fs.gen({"src": {"package": {"__init__.py": contents}}})

        file_contents = helpers.gather_file_contents(search_path=temp_fs / "src", pattern="*.py")

        assert len(file_contents) == 1
        assert file_contents[0] == (temp_fs / "src" / "package" / "__init__.py", contents)

    def test_gather_only_files(self, func_name, temp_fs_factory):
        temp_fs = temp_fs_factory.mktemp(func_name)

        contents = ""

        temp_fs.gen({"src": {"package": {"__init__.py": contents}}})

        file_contents = helpers.gather_file_contents(search_path=temp_fs / "src", pattern="*")

        assert len(file_contents) == 1
        assert file_contents[0] == (temp_fs / "src" / "package" / "__init__.py", contents)

    def test_ignore_binary_files(self, func_name, temp_fs_factory):
        temp_fs = temp_fs_factory.mktemp(func_name)

        contents = b"\r\x0fV\x00\x0c\x06\x8d\x00\x0f^\rO\x0f-\x0c\x9c\r&\x0b\xd1"

        temp_fs.gen({"binary": contents})

        file_contents = helpers.gather_file_contents(search_path=temp_fs, pattern="*")

        assert len(file_contents) == 0
