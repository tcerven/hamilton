// Copyright 2020 Tom Cervenka. All Rights Reserved.
// Derived from simple-websockets-chat-app TODO put link
const AWS = require('aws-sdk');

//global connections list
console.log('Creating connection list');
var connections=[];

exports.handler = async event => {
  const routeKey = event.requestContext.routeKey;
  console.log(`routeKey=${routeKey}`);

  if (routeKey == '$connect') {
    return onConnect(event);
  } else if (routeKey == 'sendmessage') {
    return sendMessage(event);
  } else if (routeKey == '$disconnect') {
    return onDisconnect(event);
  } else {
    return { statusCode: 500, body: 'Invalid routeKey: ' + routeKey };
  }
}

async function onConnect(event) {
  console.log(`event.requestContext.connectionId=${event.requestContext.connectionId}`);
  connections.push(event.requestContext.connectionId);
  console.log(`connections=${connections}`);
  console.log(`connections.length=${connections.length}`);
  return { statusCode: 200, body: 'Connected.' };
};

const sendMessage = async event => {
  const apigwManagementApi = new AWS.ApiGatewayManagementApi({
    apiVersion: '2018-11-29',
    endpoint: event.requestContext.domainName + '/' + event.requestContext.stage
  });

  const postData = JSON.parse(event.body);//.data;
  console.log(`postData: ${JSON.stringify(postData)}`);
  const data = postData.data;

  console.log(`connections=${connections}`);
  console.log(`connections.length=${connections.length}`);
  const postCalls = connections.map(async (connectionId) => {
    console.log(`Posting to ${connectionId}`);
    try {
      await apigwManagementApi.postToConnection({ ConnectionId: connectionId, Data: data }).promise();
      console.log(`Posted to ${connectionId}`);
      return {connectionId};
    } catch (e) {
      if (e.statusCode === 410) {
        console.log(`Found stale connection, deleting ${connectionId}`);
        return {stale: connectionId}
        // we can say that the connectionId is "deleted" because we do not push
        // the connectionId into the newConnections list
      } else {
        const msg = `postToConnection failed for connection, deleting ${connectionId}, ${e}`;
        console.error(msg);
        return {error: e};
      }
    }
  });

  try {
    let callrets = await Promise.all(postCalls);
    connections = callrets.filter(c => {
      c==undefined ? console.log(`i am undefined`) : console.log(c);
      if (c && c.connectionId) {
        return true;
      }
    });
    connections = connections.map(c => c.connectionId);
    console.log(`connections=${connections}`);

  } catch (e) {
    return { statusCode: 500, body: e.stack };
  }
  return { statusCode: 200, body: 'Data sent.' };
};

const onDisconnect = async event => {
  const index = connections.indexOf(event.requestContext.connectionId);
  if (index > -1) {
    connections.splice(index, 1);
  }
  return { statusCode: 200, body: 'Disconnected.' };
};
