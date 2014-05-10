@when(u'I go to the CBL site')
def step_impl(context):
    context.browser.get(context.testserver)


@then(u'I should see {this_content}')
def step_impl(context, this_content):
    br = context.browser
    br.get(context.testserver)
    content = br.find_element_by_id(this_content)
    assert len(content.text) > 0
