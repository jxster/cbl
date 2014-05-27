@when(u'I go to the CBL standings')
def step_impl(context):
    context.browser.get(context.testserver + '/standings')


@then(u'I should see standings as the main content')
def step_impl(context):
    page = context.parse_soup()
    assert len(page.find(id="standings")) > 0