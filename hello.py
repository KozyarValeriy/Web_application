#!/usr/bin/python3.7


def application(env, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    body = env['QUERY_STRING'].split('&')
    body = '\n'.join(body)
    start_response(status, headers)
    return [bytes(body, encoding='utf-8')]
