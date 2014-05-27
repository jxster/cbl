@when(u'I go to the CBL site')
def step_impl(context):
    context.browser.get(context.testserver)


@then(u'I should see standings on the sidebar')
def step_impl(context):
    soup = context.parse_soup()
    # content = br.find_element_by_id('standings')
    assert len(soup.find(id="standings")) > 0


@then(u'I should see recent games')
def step_impl(context):
    soup = context.parse_soup()
    assert len(soup.find(id="recent-games")) > 0
