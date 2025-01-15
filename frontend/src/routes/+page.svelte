<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { Button } from "$lib/components/ui/button";
  import { Textarea } from "$lib/components/ui/textarea";
  import * as Table from "$lib/components/ui/table";
  import * as Alert from "$lib/components/ui/alert";

  let orderMessage = "";
  const orders = writable([]);
  const itemCounts = writable({});

  let loading = writable(false);
  let alertMessage = writable(""); // State for alert message
  let alertType = writable(""); // State for alert type (success/error)

  const placeOrder = async () => {
    try {
      loading.set(true);
      alertMessage.set(""); // Reset any existing alert message
      alertType.set(""); // Reset alert type

      const response = await fetch("http://localhost:8000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ input: orderMessage }),
      });
      console.log(response);

      alertMessage.set("Request processed successfully!");
      alertType.set("success");

      setTimeout(() => {
      alertMessage.set(""); // Clear the alert message
      alertType.set(""); // Clear the alert type
      }, 5000);

      if (response.ok) {
        // Fetch the updated order and item counts after placing the order
        // const data = await response.json();
        // orders.set(data.orders);
        orderMessage = "";
        updateItemCounts();
      } else {
        console.error("Failed to place the order");
        alertMessage.set("An error occurred while placing your order.");
        alertType.set("error");
      }
    } catch (error) {
      console.error("Error placing the order", error);
      alertMessage.set("An error occurred while placing your order.");
      alertType.set("error");
    } finally {
      loading.set(false);
    }
  };

  const updateItemCounts = async () => {
    const response = await fetch("http://localhost:8000/orders");
    if (response.ok) {
      const orders_data = await response.json();
      const orders_list = [];
      const item_counts = {};
      // console.log(orders_data)

      // Loop through each order in the orders object
      for (let order_id in orders_data) {
        const order = orders_data[order_id];
        // console.log(order)
        if (order.status == "CANCELLED"){
          orders_list.push(order);
          continue
        }
        for (let item of order.items) {
          // Check if the item name exists in item_counts
          if (item.name in item_counts) {
            item_counts[item.name] += item.quantity;
          } else {
            // Initialize the count for new items
            item_counts[item.name] = item.quantity;
          }
        }

        orders_list.push(order);
      }

      // Update the itemCounts store with the calculated item counts
      itemCounts.set(item_counts);
      orders.set(orders_list);
    }
  };

  onMount(() => {
    // Initial fetch of item counts when the page loads
    updateItemCounts();
  });
</script>

<div class="center">
  <h2 class="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors mt-5">
    Order Manager
  </h2>

  <!-- Section 1: Item Counts -->
  <div class="count-section">
    {#each Object.entries($itemCounts) as [key, val]}
      <div class="card mt-3 mr-3">
        <div class="card-title">
          <h4 class="scroll-m-20 text-xl font-semibold tracking-tight">
            {key}
          </h4>
        </div>
        <div class="card-value">
          <h4 class="scroll-m-20 text-xl font-semibold tracking-tight">
            Total #{val}
          </h4>
        </div>
      </div>
    {/each}
  </div>

  <!-- Section 2: Order Form -->
  <div class="form-container">
    {#if $alertMessage}
      <!-- <div class="alert {`alert-${$alertType}`}">
        {$alertMessage}
      </div> -->
      <div class ="mb-5">
        <Alert.Root>
          <Alert.Title>{`alert-${$alertType}`}</Alert.Title>
          <Alert.Description>
            {$alertMessage}
          </Alert.Description>
        </Alert.Root>
      </div>

    {/if}
    <Textarea
      bind:value={orderMessage}
      placeholder="Enter your order details here..."
      disabled={$loading}
    ></Textarea>
    {#if $loading}
      <div class="loader"></div>
    {:else}
      <Button on:click={placeOrder}>Order</Button>
    {/if}
  </div>

  <!-- Section 3: Order Details -->
  <div>
    <h3 class="scroll-m-20 text-2xl font-semibold tracking-tight">Order History</h3>
  </div>

  <div>
    <Table.Root>
      <Table.Header>
        <Table.Row>
          <Table.Head>Order #</Table.Head>
          <Table.Head>Oder Details</Table.Head>
          <Table.Head>Status</Table.Head>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {#each $orders as order, index}
          <Table.Row>
            <Table.Cell>{order.id}</Table.Cell>
            <Table.Cell>{order.items.map((item) => `${item.quantity} ${item.name}`)}</Table.Cell>
            <Table.Cell>{order.status}</Table.Cell>
          </Table.Row>
        {/each}
      </Table.Body>
    </Table.Root>

  </div>
</div>
