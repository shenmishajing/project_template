trainer = dict(
    logger=dict(
        class_path="utils.loggers.wandb.WandbNamedLogger",
        init_args=dict(
            project="default_project_name", save_dir="work_dirs", offline=False
        ),
    ),
    callbacks=[
        dict(
            class_path="utils.progress.rich_progress.RichDefaultThemeProgressBar",
            init_args=dict(show_version=False, show_eta_time=True),
        ),
        dict(
            class_path="pytorch_lightning.callbacks.RichModelSummary",
            init_args=dict(max_depth=2),
        ),
        dict(
            class_path="utils.callbacks.wandb_logger_watch_model_callback.WandbLoggerWatchModelCallback",
            init_args=dict(log="all", log_freq=50, log_graph=False),
        ),
        dict(
            class_path="utils.callbacks.wandb_logger_log_all_code_callback.WandbLoggerLogAllCodeCallback",
            init_args=dict(root=".", name=None),
        ),
        dict(
            class_path="utils.callbacks.lr_monitor.LearningRateMonitor",
            init_args=dict(logging_interval=None, log_momentum=False),
        ),
        dict(
            class_path="utils.callbacks.model_checkpoint.ModelCheckpointWithLinkBest",
            init_args=dict(
                monitor="val/loss",
                filename=r"epoch:{epoch}-val_loss:{val/loss:.4g}",
                save_top_k=3,
                save_last=True,
                save_best=True,
                mode="min",
                auto_insert_metric_name=False,
            ),
        ),
    ],
    # debug
    limit_train_batches=1.0,
    limit_val_batches=1.0,
    limit_test_batches=1.0,
    limit_predict_batches=1.0,
    fast_dev_run=False,
    overfit_batches=0.0,
    # train
    max_epochs=None,
    min_epochs=None,
    max_steps=-1,
    min_steps=None,
    max_time=None,
    # k fold cross validation
    num_folds=None,
    # gradient clip
    gradient_clip_val=None,
    gradient_clip_algorithm=None,
    # gpus
    num_nodes=1,
    accelerator="auto",
    devices="auto",
    strategy="ddp_find_unused_parameters_false",
    # speed up
    precision=32,
    auto_lr_find=False,
    detect_anomaly=False,
    auto_scale_batch_size=False,
    accumulate_grad_batches=None,
    profiler=None,
    # val and log
    check_val_every_n_epoch=1,
    val_check_interval=1.0,
    log_every_n_steps=50,
    track_grad_norm=-1,
)

# seed
seed_everything = None
