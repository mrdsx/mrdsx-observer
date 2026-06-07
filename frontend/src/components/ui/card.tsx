import type { ComponentProps } from "solid-js";
import { splitProps } from "solid-js";

import { cx } from "@/lib/cva";

export type CardProps = ComponentProps<"div">;

export function Card(props: CardProps) {
  const [, rest] = splitProps(props, ["class"]);

  return (
    <div
      data-slot="card"
      class={cx(
        "bg-card text-card-foreground flex flex-col rounded-xl py-4 gap-4 border shadow-sm",
        props.class,
      )}
      {...rest}
    />
  );
}

export type CardHeaderProps = ComponentProps<"div">;

export function CardHeader(props: CardHeaderProps) {
  const [, rest] = splitProps(props, ["class"]);

  return (
    <div
      data-slot="card-header"
      class={cx(
        "@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start px-4 has-data-[slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-4",
        props.class,
      )}
      {...rest}
    />
  );
}

export type CardTitleProps = ComponentProps<"div">;

export function CardTitle(props: CardTitleProps) {
  const [, rest] = splitProps(props, ["class"]);

  return (
    <div
      data-slot="card-title"
      class={cx("leading-none font-semibold", props.class)}
      {...rest}
    />
  );
}

export type CardDescriptionProps = ComponentProps<"div">;

export function CardDescription(props: CardDescriptionProps) {
  const [, rest] = splitProps(props, ["class"]);

  return (
    <div
      data-slot="card-description"
      class={cx("text-muted-foreground text-sm", props.class)}
      {...rest}
    />
  );
}

export type CardActionProps = ComponentProps<"div">;

export function CardAction(props: CardActionProps) {
  const [, rest] = splitProps(props, ["class"]);

  return (
    <div
      data-slot="card-action"
      class={cx(
        "col-start-2 row-span-2 row-start-1 self-start justify-self-end",
        props.class,
      )}
      {...rest}
    />
  );
}

export type CardContentProps = ComponentProps<"div">;

export function CardContent(props: CardContentProps) {
  const [, rest] = splitProps(props, ["class"]);

  return (
    <div data-slot="card-content" class={cx("px-4", props.class)} {...rest} />
  );
}

export type CardFooterProps = ComponentProps<"div">;

export function CardFooter(props: CardFooterProps) {
  const [, rest] = splitProps(props, ["class"]);

  return (
    <div
      data-slot="card-footer"
      class={cx("flex items-center", props.class)}
      {...rest}
    />
  );
}
