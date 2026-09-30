import main


def test_main_exit(monkeypatch, capsys):
    tracker_data = {
        "next_issue_number": 1,
        "issues": []
    }

    monkeypatch.setattr(main, "load_data", lambda: tracker_data)
    monkeypatch.setattr("builtins.input", lambda _: "10")

    main.main()

    captured = capsys.readouterr()

    assert "Goodbye!" in captured.out


def test_main_invalid_option(monkeypatch, capsys):
    tracker_data = {
        "next_issue_number": 1,
        "issues": []
    }

    list_input = iter(["99", "10"])

    monkeypatch.setattr(main, "load_data", lambda: tracker_data)
    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    main.main()

    captured = capsys.readouterr()

    assert "Invalid Option" in captured.out
    assert "Goodbye!" in captured.out


def test_main_read_only_does_not_save(monkeypatch):
    tracker_data = {
        "next_issue_number": 1,
        "issues": []
    }

    calls = []

    monkeypatch.setattr(main, "load_data", lambda: tracker_data)

    monkeypatch.setitem(
        main.menu_option,
        "3",
        lambda data: calls.append("view_all")
    )

    monkeypatch.setattr(
        main,
        "save_data",
        lambda data: calls.append("save")
    )

    monkeypatch.setattr(main, "show_menu", lambda: None)

    list_input = iter(["3", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    main.main()

    assert "view_all" in calls
    assert "save" not in calls


def test_main_create_issue_saves(monkeypatch):
    tracker_data = {
        "next_issue_number": 1,
        "issues": []
    }

    calls = []

    monkeypatch.setattr(main, "load_data", lambda: tracker_data)

    monkeypatch.setitem(
        main.menu_option,
        "1",
        lambda data: calls.append("create")
    )

    monkeypatch.setattr(
        main,
        "save_data",
        lambda data: calls.append("save")
    )

    monkeypatch.setattr(main, "show_menu", lambda: None)

    list_input = iter(["1", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(list_input))

    main.main()

    assert calls == ["create", "save"]